import inspect
from copy import deepcopy
from collections import Iterable

from nio.util.logging import get_nio_logger
from nio.util.runner import Runner, RunnerStatus
from nio.signal.base import Signal


class BlockRouterNotStarted(Exception):
    pass


class InvalidBlockInput(Exception):
    pass


class InvalidBlockOutput(Exception):
    pass


class MissingBlock(Exception):
    pass


class InvalidProcessSignalsSignature(Exception):
    pass


class BlockReceiverData(object):

    """ A class that defines block receiver information,
    An instance of this class is created for each block
    receiver and accessed when delivering signals
    """

    def __init__(self, block, input_id, output_id):
        """ Create a new block receiver data.

        Take care of setting up instance variables.
        """
        self.block = block
        self.input_id = input_id
        self.output_id = output_id
        self.include_input_id = self._block_defines_input_id(block)

    def _block_defines_input_id(self, block):
        """ Returns True if the block developer can receive the input ID """
        args_spec = inspect.getargspec(block.process_signals)
        if len(args_spec.args) == 2:
            # method signature assumed to be (self, signals)
            # ==> disregard input_id even when present
            return False
        elif len(args_spec.args) == 3:
            # method signature assumed to be (self, signals, input_id)
            return True
        else:
            raise InvalidProcessSignalsSignature(
                "Block {0} signature is invalid".format(block.name))


class BlockRouter(Runner):

    """A Block Router receives service block execution information, processes
    it and becomes ready to receive signals from any participating block in
    the service execution.

    When receiving signals, the block router would be in the position of
    a speedy delivery to receiving blocks.
    """

    def __init__(self):
        """ Create a new block router instance """

        self._logger = get_nio_logger('BlockRouter')
        super().__init__(status_change_callback=self._on_status_change_callback)

        self._receivers = None
        self._clone_signals = False
        self._check_signal_type = True
        self._mgmt_signal_handler = None

    def configure(self, context):
        """Configures block router.

        This method receives the block router settings and
        it will based on these automate certain tasks so that
        signal delivery is made in an optimized fashion.

        Args:
            context (RouterContext): Context where settings are stored
        """

        self._mgmt_signal_handler = context.mgmt_signal_handler
        self._clone_signals = \
            context.settings.get("clone_signals", False)
        if self._clone_signals:
            self._logger.info('Set to clone signals for multiple receivers')
        self._check_signal_type = \
            context.settings.get("check_signal_type", True)

        """ Go through list of receivers for a given block as
        defined in "execution" entry, and parses out needed information
        to be used when delivering signals.
        """

        # cache receivers to avoid searches during signal delivery by
        # creating a dictionary of the form
        # {block_name: block instance receivers list}
        self._receivers = {}
        for block_execution in context.execution:
            # block_execution should be an instance of BlockExecution
            sender_block_name = block_execution.name()
            sender_block = context.blocks[sender_block_name]
            self._receivers[sender_block_name] = []

            # check if receivers have the {output_id: [receivers]} format
            if isinstance(block_execution.receivers(), dict):

                for output_id, block_receivers in \
                        block_execution.receivers().items():

                    # validate that output_id is valid for sender
                    if not sender_block.is_output_valid(output_id):
                        msg = "Invalid output: {0} for block: {1}".format(
                            output_id, sender_block_name)
                        self._logger.error(msg)
                        raise InvalidBlockOutput(msg)

                    parsed_receivers = \
                        self._process_receivers_list(block_receivers,
                                                     context.blocks,
                                                     output_id)
                    self._receivers[sender_block_name].extend(parsed_receivers)
            else:
                # receivers have the simple list format, i.e. [receivers]
                if sender_block._default_output is None:
                    raise InvalidBlockOutput(
                        "Block {} does not define a default output, must "
                        "specify outputs in execution config".format(
                            sender_block))
                parsed_receivers = self._process_receivers_list(
                    block_execution.receivers(),
                    context.blocks,
                    sender_block._default_output.id)
                self._receivers[sender_block_name].extend(parsed_receivers)

    def _process_receivers_list(self, receivers, blocks, output_id):
        """ Goes through and process each receiver

        Args:
            receivers: Receiver definition
            blocks (dict): instantiated service blocks
            output_id: specifies if receiver is for a given output identifier

        Returns:
            parsed list of receivers
        """
        receivers_list = []
        for receiver in receivers:
            receiver_data = self._process_block_receiver(receiver,
                                                         blocks,
                                                         output_id)
            receivers_list.append(receiver_data)

        return receivers_list

    def _process_block_receiver(self, receiver, blocks, output_id):
        """ Process a receiver component from within a list of receivers
        a block may have

        Args:
            receiver: Receiver definition
            blocks (dict): instantiated service blocks
            output_id: specifies if receiver is for a given output identifier

        Returns:
            Parsed receiver data
        """

        # determine input_id and block receiver name
        if isinstance(receiver, dict):
            try:
                input_id = receiver["input"]
                receiver_name = receiver["name"]
            except KeyError:
                self._logger.exception("Invalid format while processing block "
                                       "receiver: {0}".format(receiver))
                raise
        else:
            if receiver not in blocks:
                raise MissingBlock()
            # handling old format, get a defined input,
            # which most likely will be DEFAULT_TERMINAL
            inputs = blocks[receiver].__class__.inputs()
            # get element from set without removing it
            # TODO: Grab the default input
            input_id = next(i.id for i in inputs)
            receiver_name = receiver

        try:
            receiver_block = blocks[receiver_name]
        except KeyError as e:
            self._logger.exception(
                "Missing block for receiver: {0}".format(receiver_name))
            raise MissingBlock(e)

        # make sure input is valid for this block
        if not receiver_block.is_input_valid(input_id):
            raise InvalidBlockInput(
                "Input {} is invalid for block {}".format(
                    input_id, receiver_block))

        receiver_data = BlockReceiverData(receiver_block,
                                          input_id,
                                          output_id)
        return receiver_data

    def _on_status_change_callback(self, old_status, new_status):
        self._logger.info("Block Router status changed from: {0} to: {1}".
                          format(old_status.name, new_status.name))

    def notify_management_signal(self, block, signal):
        """The method to be called when notifying management signals

        This is called, most likely, when a block wants to notify its
        own error state.

        Args:
            block (Block): The block that is notifying.
            signal (ManagementSignal): The management signal to notify

        Return:
            None

        """
        if self._mgmt_signal_handler:
            self._mgmt_signal_handler(signal)

    def notify_signals(self, block, signals, output_id):
        """This method is called when a block is notifying signals.

        Args:
            block (Block): The block that is notifying
            signals (list): The signals that the block is notifying
            output_id: output identifier

        The signals argument is handled as follows:
            - every signal notified has to be an instance of 'Signal' by
                default, although it is configurable
            - an empty list or something evaluating to False is discarded

        """
        if self.status.is_set(RunnerStatus.started):

            if not signals:
                # discard an empty list or something that evaluates to False
                return

            if output_id is None:
                if block._default_output is None:
                    raise InvalidBlockOutput(
                        "Block does not define a default output, must "
                        "explicitly specify output in notify_signals")
                else:
                    output_id = block._default_output.id
            elif not block.is_output_valid(output_id):
                raise InvalidBlockOutput(
                    "Output {} not defined on block {}".format(
                        output_id, block))

            # make sure we can iterate
            if not isinstance(signals, Iterable):
                raise TypeError("Block Router must be able to iterate "
                                "through signals")

            # if checking Signal type (default) then
            # make sure container has signals only, quit iterating as soon as a
            # not-complying signal is found.
            if self._check_signal_type and \
               any(not isinstance(signal, Signal) for signal in signals):
                raise \
                    TypeError("All signals must be instances of Signal")

            # determine if signals are to be cloned.
            clone_signals = \
                self._clone_signals and len(self._receivers[block.name()]) > 1

            for receiver_data in self._receivers[block.name()]:
                if receiver_data.block.status.is_set(RunnerStatus.error):
                    self._logger.debug(
                        "Block '{0}' has status 'error'. Not delivering "
                        "signals from '{1}'...".format(
                            receiver_data.block.name, block.name))
                    continue
                elif receiver_data.block.status.is_set(RunnerStatus.warning):
                    self._logger.debug(
                        "Block '{0}' has status 'warning'. Delivering signals"
                        " anyway from '{1}...".format(receiver_data.block.name,
                                                      block.name))

                # We only send signals if the receiver's output matches
                # the output that these signals were notified on
                if receiver_data.output_id == output_id:
                    try:
                        signals_to_send = deepcopy(signals) \
                            if clone_signals else signals
                    except:
                        # if deepcopy fails, send original signals
                        signals_to_send = signals
                        self._logger.info("'deepcopy' operation failed while "
                                          "sending signals originating from "
                                          "block: {0}".format(block.name),
                                          exc_info=True)

                    self.deliver_signals(receiver_data, signals_to_send)

        elif self.status.is_set(RunnerStatus.stopped):
            self._logger.info("Block Router is stopped, discarding signal"
                              " notification from block: {0}".
                              format(block.name))
        elif self.status.is_set(RunnerStatus.stopping):
            self._logger.debug("Block Router is stopping, discarding signal"
                               " notification from block: {0}".
                               format(block.name))
        else:
            self._logger.warning("Block Router is not started, discarding "
                                 "signal notification from block: {0}".
                                 format(block.name))
            raise BlockRouterNotStarted()

    def deliver_signals(self, block_receiver, signals):
        """ Overridable method to deliver signals to a block

        Other block routers can override this method to perform special actions
        when delivering signals to a block. It is recommended to call the
        block router's notify_signals_to_block method from this method though,
        as that takes care of handling different formats of blocks.

        Args:
            block_receiver (BlockReceiverData): The data about the block that
                will be receiving the signals
            signals (Iterable): The signals that the block will receive
        """
        self.notify_signals_to_block(block_receiver, signals)

    def notify_signals_to_block(self, block_receiver, signals):
        """ Call process signals on a block with the proper signature.

        Block developers are not required to include an input_id in their
        block's process_signals function definition. This method will
        """
        # Check if the block has defined the input_id in its process_signals
        if block_receiver.include_input_id:
            # Pass the block_receiver's input_id to the process_signals method
            block_receiver.block.process_signals(
                signals, block_receiver.input_id)
        else:
            # Only send the signals to the block, no input_id
            block_receiver.block.process_signals(signals)

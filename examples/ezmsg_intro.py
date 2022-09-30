## Ezmsg Introduction

# If this is your first time using ezmsg, you're in the right place. 
# This script will walk through the basics of creating a very simple 
# ezmsg system. ezmsg is ideal for creating modular processing 
# pipelines whose steps can be arranged as a directed acyclic graph. 
# In this script, we will walk through a very simple graph which 
# generates a count of numbers, adds 1 to each number, and prints to 
# standard output.

# We will write an ezmsg Unit for each discrete step of our pipeline, 
# and connect them together with a System.

import ezmsg.core as ez
from typing import AsyncGenerator

# Create a message type to pass between the Units. The message type 
# should inherit from Message.

class CountMessage(ez.Message):
    value: int

# We also need a way to tell the Unit how many numbers to generate.

class CountSettings(ez.Settings):
   iterations: int

# Next, create a Unit that will generate the count. Every Unit should 
# contain inputs and/or outputs and at least one function which 
# subscribes to the inputs or publishes to the outputs.

# For Count, we create an OutputStream and a publishing function which 
# will perform the number calculation and yield CountMessages to the 
# OutputStream.

class Count(ez.Unit):

    SETTINGS: CountSettings    # Declare Settings, do not instantiate

    OUTPUT_COUNT = ez.OutputStream(CountMessage)

    @ez.publisher(OUTPUT_COUNT)
    async def count(self) -> AsyncGenerator:
        count = 0
        while count < self.SETTINGS.iterations:
            yield (self.OUTPUT_COUNT, CountMessage(
                value=count
            ))
            count = count + 1

# The next `Unit` in the chain should accept a `CountMessage` from the 
# first `Unit`, add 1 to its value, and yield a new CountMessage. To 
# do this, we create a new `Unit` which contains a function which both 
# subscribes and publishes. We will connect this `Unit` to `Count` 
# later on, when we create a `System`.

# The subscribing function will be called anytime the `Unit` receives 
# a message to the `InputStream` that the function subscribes to. In 
# this case, `INPUT_COUNT`.

class AddOne(ez.Unit):

    INPUT_COUNT = ez.InputStream(CountMessage)
    OUTPUT_PLUS_ONE = ez.OutputStream(CountMessage)

    @ez.subscriber(INPUT_COUNT)
    @ez.publisher(OUTPUT_PLUS_ONE)
    async def on_message(self, message) -> AsyncGenerator:
        yield (self.OUTPUT_PLUS_ONE, CountMessage(
            value=message.value + 1
        ))

# Finally, the last unit should print the value of any messages it 
# receives.

# Since this unit is the last in the pipeline, it should also
# terminate the system when it receives the last message. We can use
# `ez.NormalTermination` to let the system know that it should
# gracefully shut down.

# We can use both Settings and State together to count messages and
# raise `ez.NormalTermination` when all have passed through.

class PrintSettings(ez.Settings):
    iterations: int

class PrintState(ez.State):
    current_iteration: int = 0

class PrintValue(ez.Unit):

    SETTINGS: PrintSettings
    STATE: PrintState

    INPUT = ez.InputStream(CountMessage)

    @ez.subscriber(INPUT)
    async def on_message(self, message) -> None:

        print(message.value)

        self.STATE.current_iteration = self.STATE.current_iteration + 1
        if self.STATE.current_iteration == self.SETTINGS.iterations:
            raise ez.NormalTermination

# The last thing to do before we have a fully functioning ezmsg 
# pipeline is to define any Settings that have been declared and to 
# connect all of the units together. We do this using a System. The 
# configure() and network() functions are special functions that 
# define System behavior.

class CountSystemSettings(ez.Settings):
    iterations: int

class CountSystem(ez.System):

    SETTINGS: CountSystemSettings

    # Define member units
    COUNT = Count()
    ADD_ONE = AddOne()
    PRINT = PrintValue()

    # Use the configure function to apply settings to member Units
    def configure(self) -> None:
        self.COUNT.apply_settings(
            CountSettings(iterations=self.SETTINGS.iterations)
        )
        
        self.PRINT.apply_settings(
            PrintSettings(iterations=self.SETTINGS.iterations)
        )

    # Use the network function to connect inputs and outputs of Units
    def network(self) -> ez.NetworkDefinition:
        return (
            (self.COUNT.OUTPUT_COUNT, self.ADD_ONE.INPUT_COUNT),
            (self.ADD_ONE.OUTPUT_PLUS_ONE, self.PRINT.INPUT)
        )

# Finally, instantiate and run the system!

if __name__ == "__main__":
    settings = CountSystemSettings(iterations=20)
    system = CountSystem(settings)
    ez.run_system(system)
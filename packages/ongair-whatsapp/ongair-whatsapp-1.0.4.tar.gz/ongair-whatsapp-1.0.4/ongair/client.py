from util import setup_logging, get_env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers.protocol_receipts import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks import YowAckProtocolLayer
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.coder import YowCoderLayer
from yowsup.layers.protocol_media import YowMediaProtocolLayer
from yowsup.stacks import YowStack
from yowsup.stacks import YowStackBuilder
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup.layers import YowParallelLayer
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS
from yowsup import env
from ongair import OngairLayer
from stack import OngairStackBuilder


class Client:
    def __init__(self, phone_number, encrypted=True):
        self.connected = False
        self.encrypted = encrypted
        self.phone_number = phone_number

        setup_logging(phone_number)

    def loop(self):
        if self.encrypted:
            stackBuilder = YowStackBuilder()
            # Create the default stack (a pile of layers) and add the Ongair Layer to the top of the stack
            stack = stackBuilder.pushDefaultLayers(True).push(OngairLayer).build()

            # Set the phone number as a property that can be read by other layers
            stack.setProp('ongair.account', self.phone_number)
            stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])  # whatsapp server address
            stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
            stack.setProp(YowCoderLayer.PROP_RESOURCE,
                          env.CURRENT_ENV.getResource())  # info about us as WhatsApp client

            # Broadcast the login event. This gets handled by the OngairLayer
            stack.broadcastEvent(YowLayerEvent(OngairLayer.EVENT_LOGIN))

            # Run the asyncore loop
            stack.loop(timeout=5, discrete=0.5)  # this is the program mainloop
        else:
            # in the case that it is not encrypted
            # TODO: Refactor this if necessary
            stackBuilder = OngairStackBuilder()
            stack = stackBuilder.pushDefaultLayers().push(OngairLayer).build()

            stack.setProp('ongair.account', self.phone_number)
            stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])  # whatsapp server address
            stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
            stack.setProp(YowCoderLayer.PROP_RESOURCE,
                          env.CURRENT_ENV.getResource())  # info about us as WhatsApp client
            stack.broadcastEvent(YowLayerEvent(OngairLayer.EVENT_LOGIN))
            stack.loop(timeout=5, discrete=0.5)  # this is the program mainloop

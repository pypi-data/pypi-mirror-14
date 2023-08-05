from cryptoconditions.buffer import MAX_SAFE_INTEGER_JS


class BitmaskRegistry:
    registered_types = []

    @staticmethod
    def get_class_from_typebit(bitmask):
        """
        Determine fulfillment implementation class from a bitmask.

        Returns the class implementing a fulfillment type that matches a certain bitmask.

        Args:
           bitmask (int): fulfillment bitmask

        Return:
            Class implementing the given fulfillment type.
        """
        # Determine type of condition
        if bitmask > MAX_SAFE_INTEGER_JS:
            raise ValueError('Bitmask {} is not supported'.format(bitmask))

        for registered_type in BitmaskRegistry.registered_types:
            if bitmask == registered_type['bitmask']:
                return registered_type['class']

        raise ValueError('Bitmask {} is not supported'.format(bitmask))

    @staticmethod
    def register_type(cls):
        """
        Add a new fulfillment type.

        This can be used to extend this cryptocondition implementation with new
        fulfillment types that it does not yet support. But mostly it is used
        internally to register the built-in types.

        In this method, we expect a regular fulfillment type, for information on
        registering meta types please see `registerMetaType`.

        Args:
           cls: Implementation of a fulfillment type.
        """
        # TODO Do some sanity checks on Class

        BitmaskRegistry.registered_types.append(
            {
                'bitmask': cls().bitmask,
                'class': cls
            })


from cryptoconditions.fulfillments.sha256 import Sha256Fulfillment
from cryptoconditions.fulfillments.threshold_sha256 import ThresholdSha256Fulfillment
from cryptoconditions.fulfillments.ed25519_sha256 import Ed25519Sha256Fulfillment

BitmaskRegistry.register_type(Sha256Fulfillment)
BitmaskRegistry.register_type(ThresholdSha256Fulfillment)
BitmaskRegistry.register_type(Ed25519Sha256Fulfillment)

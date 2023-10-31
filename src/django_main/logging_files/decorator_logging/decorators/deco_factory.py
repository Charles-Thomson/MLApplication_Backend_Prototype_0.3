class PreAndPostCallFuncationFactory:
    """
    Factory for the pre and post call functions
    This file is not currently used but is kept for future use
    """

    function_types = {}

    @classmethod
    def get_pre_and_post_call_function(cls, function_type: str):
        """
        Get the pre call function based on function type
        var: function_type - Desired type of pre and post call functions
        rtn: pre_call - the pre_call function of desired type
        rtn: post_call - the post_call function of desired type
        """
        try:
            pre_call = cls.function_types["pre_call_" + function_type]
            post_call = cls.function_types["post_call_" + function_type]

        except KeyError as err:
            raise NotImplementedError(
                f"Not implemented{function_type} as either pre or post call funciton"
            ) from err

        return pre_call, post_call

    @classmethod
    def register_pre_call_function(cls, type_name):
        """
        Register a function type as a deco
        var: type_name - the type of function registered
        """

        def deco(deco_cls):
            cls.function_types["pre_call_" + type_name] = deco_cls

            return deco

    @classmethod
    def register_post_call_function(cls, type_name):
        """
        Register a function type as a deco
        var: type_name - the type of function registered
        """

        def deco(deco_cls):
            cls.function_types["post_call_" + type_name] = deco_cls

            return deco
        
class FunctionDecoratorFactory:
    """
    Factory for the generation of logging decorators
    """

    function_decos = {}

    @classmethod
    def get_decerator(cls, deco_type: str, pre_and_and_post_call_type: str):
        """
        Get the pre call function based on function type
        var: function_type - Desired type of pre and post call functions
        rtn: pre_call - the pre_call function of desired type
        rtn: post_call - the post_call function of desired type
        """
        try:
            decorator = cls.function_types[]
        
        except KeyError as err:
            raise NotImplementedError(
                f"Not implemented{function_type} as either pre or post call funciton"
            ) from err

        return pre_call, post_call

    @classmethod
    def register_pre_call_function(cls, type_name):
        """
        Register a function type as a deco
        var: type_name - the type of function registered
        """

        def deco(deco_cls):
            cls.function_types["pre_call_" + type_name] = deco_cls

            return deco
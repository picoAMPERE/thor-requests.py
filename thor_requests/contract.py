""" Contract is a representation of an underlying Solidity compiled JSON """
from typing import Union, List
from .utils import read_json_file
from thor_devkit import abi


class Contract:
    def __init__(self, meta_dict: dict):
        self.contract_meta: dict = meta_dict

    @classmethod
    def fromFile(cls, path_or_str):
        meta_dict = read_json_file(path_or_str)
        return cls(meta_dict)

    def get_contract_name(self) -> Union[str, None]:
        """Get the smart contract name, or None"""
        return self.contract_meta.get("contractName")

    def get_bytecode(self, key: str = "bytecode") -> bytes:
        """Get bytecode of this smart contract"""
        return bytes.fromhex(self.contract_meta[key])

    def get_abis(self) -> List[dict]:
        """Get ABIs of this contract as a list of dicts"""
        return self.contract_meta["abi"]

    def get_abi(self, func_name: str) -> Union[dict, None]:
        """Get specific ABI in dict form by function/event name, or None if not found"""
        abis = self.get_abis()
        targets = [each for each in abis if each.get("name") == func_name]
        assert len(targets) <= 1  # Zero or at most, one found.
        if len(targets):
            return targets[0]
        else:
            return None

    def get_function_by_name(
        self, func_name: str, strict_mode=False
    ) -> Union[abi.Function, None]:
        """
        Get a function instance by its name, or None if not found

        In strict mode, it willl raise if function not found.
        """
        abi_dict = self.get_abi(func_name)
        if not abi_dict and strict_mode:
            raise Exception(f"Function {func_name} not found on the contract")

        if not abi_dict:
            return None

        f = abi.Function(abi_dict)
        return f

    def get_events(self) -> List[abi.Event]:
        """Get events from the abi sections"""
        return [
            abi.Event(each) for each in self.get_abis() if each.get("type") == "event"
        ]

    def get_event_by_signature(self, signature: bytes) -> Union[abi.Event, None]:
        """
        Get target event from contract meta by signatuer string.

        Parameters
        ----------
        signature : bytes
            32 bytes
        """
        events_obj_list = self.get_events()
        events_dict = {each.get_signature(): each for each in events_obj_list}
        if signature in events_dict:
            return events_dict[signature]
        else:
            return None

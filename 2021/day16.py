import aoc_util as aoc
import operator
import utility.util as util

from functools import reduce

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        hex_code = aoc.parse_input(puzzle_input)[0]
        bin_code = "".join(util.convert_hex_to_bin(char) for char in hex_code)

        self.packets, _ = self.parse_packets(bin_code)

    def part1(self) -> tuple[str, (int | str)]:
        solution = self.get_version_sum(self.packets)
        return f"Sum of packet versions: {solution}", solution

    def part2(self) -> tuple[str, (int | str)]:
        if len(self.packets) > 1:
            raise RuntimeError("'packets' can't be interpreted. There is more than one root package.")

        solution = self.interpret_packet(self.packets[0])
        return f"Value of encoded transmission: {solution}", solution

    def parse_packets(self, bin_code: str, max_packets_size: int=0) -> tuple[list[dict], int]:
        packets = []
        current_pos = 0

        while current_pos < len(bin_code) and "1" in bin_code[current_pos :]:
            # get packet version
            packet = {}
            packet["version"] = int(bin_code[current_pos : current_pos+3], base=2)
            current_pos += 3

            # get packet type id
            packet["id"] = int(bin_code[current_pos : current_pos+3], base=2)
            current_pos += 3

            # literal
            if packet["id"] == 4:
                number_string = ""
                while True:
                    number_string += bin_code[current_pos+1 : current_pos+5]

                    current_pos += 5

                    if bin_code[current_pos-5] == "0":
                        break

                if number_string == "":
                    number_string = "0"

                packet["value"] = int(number_string, base=2)
            
            # operator
            else:
                packet["length_type"] = int(bin_code[current_pos])
                current_pos += 1

                if packet["length_type"] == 0:
                    packet["subpackets_length"] = int(bin_code[current_pos : current_pos+15], base=2)
                    current_pos += 15
                    packet["subpackets"], consumed_bits = self.parse_packets(bin_code[current_pos : current_pos+packet["subpackets_length"]])
                elif packet["length_type"] == 1:
                    packet["subpackets_length"] = int(bin_code[current_pos : current_pos+11], base=2)
                    current_pos += 11
                    packet["subpackets"], consumed_bits = self.parse_packets(bin_code[current_pos :], packet["subpackets_length"])
                else:
                    raise RuntimeError(f"Unsupported Length Type: {packet['length_type']}")

                current_pos += consumed_bits

            packets.append(packet)

            if (max_packets_size > 0) and (len(packets) >= max_packets_size):
                break

        return packets, current_pos

    def interpret_packet(self, packet: dict) -> int:
        match packet["id"]:
            case 0:
                return sum([self.interpret_packet(subpacket) for subpacket in packet["subpackets"]])
            case 1:
                return reduce(operator.mul, [self.interpret_packet(subpacket) for subpacket in packet["subpackets"]])
            case 2:
                return min([self.interpret_packet(subpacket) for subpacket in packet["subpackets"]])
            case 3:
                return max([self.interpret_packet(subpacket) for subpacket in packet["subpackets"]])
            case 5:
                return 1 if self.interpret_packet(packet["subpackets"][0]) > self.interpret_packet(packet["subpackets"][1]) else 0
            case 6:
                return 1 if self.interpret_packet(packet["subpackets"][0]) < self.interpret_packet(packet["subpackets"][1]) else 0
            case 7:
                return 1 if self.interpret_packet(packet["subpackets"][0]) == self.interpret_packet(packet["subpackets"][1]) else 0
            case _:
                return packet["value"]

    def get_version_sum(self, packets: list[dict]) -> int:
        version_sum = 0
        for packet in packets:
            version_sum += packet["version"]

            if "subpackets" in packet:
                version_sum += self.get_version_sum(packet["subpackets"])

        return version_sum
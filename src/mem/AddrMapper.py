# Copyright (c) 2012 ARM Limited
# All rights reserved.
#
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from m5.params import *
from m5.SimObject import SimObject


# An address mapper changes the packet addresses in going from the
# response port side of the mapper to the request port side. When the
# response port is queried for the address ranges, it also performs the
# necessary range updates. Note that snoop requests that travel from
# the request port (i.e. the memory side) to the response port are
# currently not modified.
class AddrMapper(SimObject):
    type = "AddrMapper"
    cxx_header = "mem/addr_mapper.hh"
    cxx_class = "gem5::AddrMapper"
    abstract = True

    # one port in each direction
    mem_side_port = RequestPort(
        "This port sends requests and receives responses"
    )
    master = DeprecatedParam(
        mem_side_port, "`master` is now called `mem_side_port`"
    )
    cpu_side_port = ResponsePort(
        "This port receives requests and sends responses"
    )
    slave = DeprecatedParam(
        cpu_side_port, "`slave` is now called `cpu_side_port`"
    )


# Range address mapper that maps a set of original ranges to a set of
# remapped ranges, where a specific range is of the same size
# (original and remapped), only with an offset.
class RangeAddrMapper(AddrMapper):
    type = "RangeAddrMapper"
    cxx_header = "mem/addr_mapper.hh"
    cxx_class = "gem5::RangeAddrMapper"

    # These two vectors should be the exact same length and each range
    # should be the exact same size. Each range in original_ranges is
    # mapped to the corresponding element in the remapped_ranges. Note
    # that the same range can occur multiple times in the remapped
    # ranges for address aliasing.
    original_ranges = VectorParam.AddrRange(
        "Ranges of memory that should me remapped"
    )
    remapped_ranges = VectorParam.AddrRange(
        "Ranges of memory that are being mapped to"
    )


def generate_identity_matrix(size):
    """Generate an identity matrix of the given size as a list of unsigned integers."""
    return [(1 << i) for i in range(size)]


class MatrixAddrMapper(AddrMapper):
    type = "MatrixAddrMapper"
    cxx_class = "gem5::MatrixAddrMapper"
    cxx_header = "mem/addr_mapper.hh"

    # The binary invertible matrix as a list of unsigned integers.
    bim = VectorParam.UInt64(
        generate_identity_matrix(64), "Binary Invertible Matrix"
    )

    bim_inv = VectorParam.UInt64(
        generate_identity_matrix(64), "Inverse of the Binary Invertible Matrix"
    )

    # The size of the address (number of bits).
    N = Param.Int(64, "Size of the address (number of bits)")

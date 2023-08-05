from __future__ import absolute_import
from __future__ import print_function
import sys
import os

# the next line can be removed after installation
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from veriloggen import *

def mkLed():
    m = Module('blinkled')
    clk = m.Input('CLK')
    rst = m.Input('RST')
    valid = m.OutputReg('valid', initval=0)
    count = m.Reg('count', width=32, initval=0)
    
    fsm = FSM(m, 'fsm', clk, rst)
    
    for i in range(4):
        fsm.goto_next()

    # condition alias
    c = count >= 16

    # assert valid if the condition is satisfied
    # then de-assert 3 cycles later with same condition
    fsm.add( valid(1), cond=c, keep=3)
    fsm.add( valid(0), cond=c, delay=3)
    fsm.goto_next(cond=c)
    
    for i in range(8):
        fsm.goto_next()

    # condition alias
    c = count >= 32

    # assert valid 1 cycle later if the condition is satisfied now
    # then de-assert 4 cycles later with same condition
    for i in range(8):
        fsm.add( valid(1), cond=c, delay=1, keep=3)
        fsm.add( valid(0), cond=c, delay=4 )
        fsm.goto_next(cond=c)

    fsm.make_always(reset=[count.reset()], body=[count(count+1)])
        
    return m

def mkTest():
    m = Module('test')
    clk = m.Reg('CLK')
    rst = m.Reg('RST')
    valid = m.Wire('valid')

    uut = m.Instance(mkLed(), 'uut',
                     ports=(('CLK', clk), ('RST', rst), ('valid', valid)))

    simulation.setup_waveform(m, uut)
    simulation.setup_clock(m, clk, hperiod=5)
    init = simulation.setup_reset(m, rst, period=100)

    init.add(
        Delay(1000),
        Systask('finish'),
    )

    return m
    
if __name__ == '__main__':
    test = mkTest()
    verilog = test.to_verilog('tmp.v')
    print(verilog)

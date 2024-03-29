from TUM_quantum_sim.Dual_QW import main as Dual_QW
from TUM_quantum_sim.exam import main as exam
from TUM_quantum_sim.QB import main as QB
from TUM_quantum_sim.QCL import main as QCL
from TUM_quantum_sim.QW_sim import main as QW
from TUM_quantum_sim.RTD_sim import main as RTD
from TUM_quantum_sim.SQUID import main as SQUID

if __name__ == "__main__":
    RTD.main()
    QW.main()
    SQUID.main()
    Dual_QW.main()
    QCL.main()
    QB.main()
    exam.main()

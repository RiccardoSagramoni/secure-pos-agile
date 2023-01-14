import sys

from testing_system.tester_elasticity import ElasticityTester
from testing_system.tester_execution import ExecutionTester


def execution_testing():
    test_system = ExecutionTester()
    execution_len = 1000
    monitoring_len = 10

    # num_sessions = [5]
    num_sessions = [i * (execution_len + monitoring_len) for i in range(1, 5)]
    
    test_system.start_execution_testing(num_sessions, execution_len, monitoring_len)

    
def elasticity_testing():
    test_system = ElasticityTester()
    how_many_classifier = [5, 10, 15, 20, 25]
    test_system.start_development_testing(how_many_classifier)


if __name__ == "__main__":
    # execution_testing()
    elasticity_testing()
    print("FINE TESTING")
    sys.exit(0)

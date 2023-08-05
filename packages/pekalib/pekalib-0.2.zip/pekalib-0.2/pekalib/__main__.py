from robotremoteserver import RobotRemoteServer
from .base import PekaLib


def main():
    RobotRemoteServer(PekaLib())


if __name__ == '__main__':
    main()

from tscli import TensorClient
import define_parties


def main():
    client = TensorClient(define_parties.servring_addr0)
    resp = client.expressions()
    print(resp)


if __name__ == "__main__":
    main()

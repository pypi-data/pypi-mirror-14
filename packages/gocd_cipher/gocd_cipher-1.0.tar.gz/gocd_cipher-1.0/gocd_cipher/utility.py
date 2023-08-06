import argparse
import sys

from gocd_cipher.crypto import gocd_encrypt, gocd_decrypt, gocd_reencrypt


def utility():
    parser = argparse.ArgumentParser(usage="""
        A utility to encrypt, decrypt or reencrypt a secret for use with GoCD.
    """)
    subparser = parser.add_subparsers()
    encyrpt = subparser.add_parser("encrypt",
                                   help="Encrypt plaintext with a GoCD cipher key")
    encyrpt.add_argument("--key",
                         help="A hex encoded GoCD cipher key as found in /etc/go/cipher",
                         required=True)
    encyrpt.add_argument("--plaintext",
                         help="The text to encrypt. If this is not passed, the utility operates in interactive mode.")
    encyrpt.set_defaults(mode="encrypt")
    decrypt = subparser.add_parser("decrypt",
                                   help="Decrypt a secret with a GoCD cipher key")
    decrypt.add_argument("--key",
                         help="A hex encoded GoCD cipher key as found in /etc/go/cipher",
                         required=True)
    decrypt.add_argument("--ciphertext",
                         help="The text to decrypt. If this is not passed, the utility operates in interactive mode.")
    decrypt.set_defaults(mode="decrypt")
    reencrypt = subparser.add_parser("reencrypt",
                                     help="Decrypt a secret with one GoCD cipher key, and reencrypt it with another")
    reencrypt.add_argument("--old_key",
                           help="A hex encoded GoCD cipher key as found in /etc/go/cipher, used to encrypt the ciphertext",
                           required=True)
    reencrypt.add_argument("--new_key",
                           help="A hex encoded GoCD cipher key as found in /etc/go/cipher, to encrypt the secret with",
                           required=True)
    reencrypt.add_argument("--ciphertext",
                           help="The text to reencrypt. If this is not passed, the utility operates in interactive mode.")
    reencrypt.set_defaults(mode="reencrypt")
    args = parser.parse_args()
    if args.mode == "encrypt":
        if args.plaintext:
            sys.stdout.write(gocd_encrypt(args.key, args.plaintext))
        else:
            while True:
                try:
                    sys.stdout.write(gocd_encrypt(args.key, raw_input()))
                    sys.stdout.write("\n")
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print e
    elif args.mode == "decrypt":
        if args.ciphertext:
            sys.stdout.write(gocd_decrypt(args.key, args.ciphertext))
        else:
            while True:
                try:
                    sys.stdout.write(gocd_decrypt(args.key, raw_input()))
                    sys.stdout.write("\n")
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print e
    elif args.mode == "reencrypt":
        if args.ciphertext:
            sys.stdout.write(gocd_reencrypt(args.old_key, args.new_key, args.ciphertext))
        else:
            while True:
                try:
                    sys.stdout.write(gocd_reencrypt(args.old_key, args.new_key, raw_input()))
                    sys.stdout.write("\n")
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print e
    else:
        sys.stderr.write("You must pass one of encrypt, decrypt or reencrypt as a mode.\n")
        sys.stderr.flush()
        sys.exit(1)
    sys.stdout.flush()
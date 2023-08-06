import json
import ecdsa
import datetime
from keylib import ECPrivateKey, ECPublicKey, public_key_to_address
from jsontokens import TokenSigner, TokenVerifier, decode_token


def verify_token_record(token_record, verifier,
                        signing_algorithm="ES256"):
    """ A function for validating an individual token record and extracting
        the decoded token.
    """

    if not ("token" in token_record and "publicKey" in token_record and \
            "parentPublicKey" in token_record):
        raise ValueError("Invalid token record")

    token = token_record["token"]
    token_record_public_key = str(token_record["publicKey"])

    if verifier == token_record_public_key:
        pass
    elif verifier == public_key_to_address(token_record_public_key):
        pass
    else:
        raise ValueError("Token public key doesn't match")

    public_key = ECPublicKey(token_record_public_key)

    token_verifier = TokenVerifier()
    token_is_valid = token_verifier.verify(token, public_key.to_pem())
    if not token_is_valid:
        raise ValueError("Token is not valid")

    decoded_token = decode_token(token)
    decoded_token_payload = decoded_token["payload"]

    if "subject" not in decoded_token_payload:
        raise ValueError("Invalid decoded token")
    if "publicKey" not in decoded_token_payload["subject"]:
        raise ValueError("Invalid decoded token")
    if "claim" not in decoded_token_payload:
        raise ValueError("Invalid decoded token")

    if token_record["publicKey"] == token_record["parentPublicKey"]:
        if token_record["publicKey"] != decoded_token_payload["subject"]["publicKey"]:
            raise ValueError("Token's public key doesn't match")
    else:
        raise ValueError(
            "Verification of tokens signed with keychains is not yet supported")

    return decoded_token


def get_profile_from_tokens(token_records, public_key_or_address,
                            hierarchical_keys=False):
    """ A function for extracting a profile from a list of tokens.
    """
    
    if hierarchical_keys:
        raise NotImplementedError("Hierarchical key support not implemented")

    profile = {}

    for token_record in token_records:
        try:
            decoded_token = verify_token_record(token_record, public_key_or_address)
        except ValueError:
            continue
        else:
            if "payload" in decoded_token:
                if "claim" in decoded_token["payload"]:
                    claim = decoded_token["payload"]["claim"]
                    profile.update(claim)

    return profile

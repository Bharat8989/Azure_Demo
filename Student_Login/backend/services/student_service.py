import base64
import hashlib
import hmac
import json
import secrets
import time
import uuid

from config.config import Config
from models.student import Student
from repositories.student_repo import StudentRepository


class StudentService:

    def __init__(
        self,
        repository: StudentRepository
    ):
        self.repository = repository

    # ---------------------------------------------------------
    # Password hashing
    # ---------------------------------------------------------

    def hash_password(
        self,
        password: str
    ) -> str:

        salt = secrets.token_bytes(16)

        derived_key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            210_000
        )

        return (
            "pbkdf2_sha256$210000$"
            f"{base64.urlsafe_b64encode(salt).decode()}"
            "$"
            f"{base64.urlsafe_b64encode(derived_key).decode()}"
        )

    def verify_password(
        self,
        password: str,
        stored_hash: str
    ) -> bool:

        try:

            algorithm, iterations, salt_b64, hash_b64 = (
                stored_hash.split("$")
            )

            if algorithm != "pbkdf2_sha256":
                return False

            salt = base64.urlsafe_b64decode(
                salt_b64
            )

            expected_hash = base64.urlsafe_b64decode(
                hash_b64
            )

            actual_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt,
                int(iterations)
            )

            return hmac.compare_digest(
                actual_hash,
                expected_hash
            )

        except (
            ValueError,
            TypeError
        ):
            return False

    # ---------------------------------------------------------
    # Register
    # ---------------------------------------------------------

    def register(
        self,
        name: str,
        email: str,
        password: str
    ):

        normalized_name = name.strip()
        normalized_email = email.strip().lower()

        if self.repository.exists_by_email(
            normalized_email
        ):
            raise ValueError(
                "An account with this email already exists."
            )

        student = Student(
            student_id=str(uuid.uuid4()),
            name=normalized_name,
            email=normalized_email,
            password_hash=self.hash_password(password),
            is_active=True
        )

        return self.repository.create(student)

    # ---------------------------------------------------------
    # Login
    # ---------------------------------------------------------

    def login(
        self,
        email: str,
        password: str
    ):

        normalized_email = email.strip().lower()

        student = self.repository.get_by_email(
            normalized_email
        )

        if not student:
            return None

        if not student.is_active:
            return None

        if not self.verify_password(
            password,
            student.password_hash
        ):
            return None

        token = self.generate_token(
            student.student_id
        )

        return {
            "token": token,
            "student": student.to_dict()
        }

    # ---------------------------------------------------------
    # Token helpers
    # ---------------------------------------------------------

    def _base64url_encode(
        self,
        value: bytes
    ) -> str:

        return (
            base64.urlsafe_b64encode(value)
            .decode()
            .rstrip("=")
        )

    def _base64url_decode(
        self,
        value: str
    ) -> bytes:

        padding = "=" * (-len(value) % 4)

        return base64.urlsafe_b64decode(
            value + padding
        )

    def generate_token(
        self,
        student_id: str
    ) -> str:

        now = int(time.time())

        expires_at = (
            now +
            Config.JWT_EXPIRATION_SECONDS
        )

        header = {
            "alg": "HS256",
            "typ": "JWT"
        }

        payload = {
            "sub": student_id,
            "iat": now,
            "exp": expires_at
        }

        header_encoded = self._base64url_encode(
            json.dumps(
                header,
                separators=(",", ":")
            ).encode()
        )

        payload_encoded = self._base64url_encode(
            json.dumps(
                payload,
                separators=(",", ":")
            ).encode()
        )

        unsigned_token = (
            f"{header_encoded}.{payload_encoded}"
        )

        signature = hmac.new(
            Config.SECRET_KEY.encode(),
            unsigned_token.encode(),
            hashlib.sha256
        ).digest()

        signature_encoded = self._base64url_encode(
            signature
        )

        return (
            f"{unsigned_token}.{signature_encoded}"
        )

    def verify_token(
        self,
        token: str
    ):

        try:

            parts = token.split(".")

            if len(parts) != 3:
                return None

            (
                header_encoded,
                payload_encoded,
                signature_encoded
            ) = parts

            unsigned_token = (
                f"{header_encoded}.{payload_encoded}"
            )

            expected_signature = hmac.new(
                Config.SECRET_KEY.encode(),
                unsigned_token.encode(),
                hashlib.sha256
            ).digest()

            provided_signature = (
                self._base64url_decode(
                    signature_encoded
                )
            )

            if not hmac.compare_digest(
                expected_signature,
                provided_signature
            ):
                return None

            payload = json.loads(
                self._base64url_decode(
                    payload_encoded
                )
            )

            if int(payload.get("exp", 0)) < int(time.time()):
                return None

            student_id = payload.get("sub")

            if not student_id:
                return None

            student = self.repository.get_by_id(
                student_id
            )

            if not student:
                return None

            if not student.is_active:
                return None

            return student

        except (
            ValueError,
            TypeError,
            json.JSONDecodeError,
            UnicodeDecodeError
        ):
            return None

    # ---------------------------------------------------------
    # Forget password
    # ---------------------------------------------------------

    def request_password_reset(
        self,
        email: str
    ):

        normalized_email = email.strip().lower()

        student = self.repository.get_by_email(
            normalized_email
        )

        # Do not reveal whether account exists.
        if not student:
            return

        reset_token = secrets.token_urlsafe(32)

        expires_at = (
            time.time() + 900
        )

        student.reset_token = reset_token

        student.reset_token_expires_at = (
            expires_at
        )

        self.repository.update(student)

        # Mock email operation
        print(
            "[PASSWORD RESET MOCK]"
        )

        print(
            f"Email: {student.email}"
        )

        print(
            f"Reset Token: {reset_token}"
        )
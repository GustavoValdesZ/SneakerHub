document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');

    // Validators
    const validators = {
        first_name: (value) => {
            if (value.length < 3 || value.length > 15) return "El nombre debe tener entre 3 y 15 letras.";
            if (!/^[a-zA-Z]+$/.test(value)) return "El nombre solo debe contener letras.";
            return null;
        },
        last_name: (value) => {
            if (value.length < 3 || value.length > 15) return "El apellido debe tener entre 3 y 15 letras.";
            if (!/^[a-zA-Z]+$/.test(value)) return "El apellido solo debe contener letras.";
            return null;
        },
        email: (value) => {
            if (!value.includes('@')) return "El correo debe contener '@'.";
            // Simple regex for email structure
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return "Ingrese un correo electrónico válido.";
            return null;
        },
        password: (value) => {
            if (value.length < 4 || value.length > 20) return "La contraseña debe tener entre 4 y 20 caracteres.";
            if (!/[A-Z]/.test(value)) return "La contraseña debe contener al menos 1 mayúscula.";
            if (!/[0-9]/.test(value)) return "La contraseña debe contener al menos 1 número.";
            if (!/[!@#$%^&*(),.?":{}|<>]/.test(value)) return "La contraseña debe contener al menos 1 carácter especial.";
            return null;
        },
        confirm_password: (value, form) => {
            const password = form.querySelector('[name="password"]').value;
            if (value !== password) return "Las contraseñas no coinciden.";
            return null;
        }
    };

    function validateField(input, form) {
        const fieldName = input.name;
        const errorElement = document.getElementById(`error-${fieldName}`);

        if (validators[fieldName]) {
            const errorMessage = validators[fieldName](input.value, form);
            if (errorMessage) {
                errorElement.textContent = errorMessage;
                errorElement.style.display = 'block';
                input.style.borderColor = '#ff6b6b';
                return false;
            } else {
                errorElement.style.display = 'none';
                input.style.borderColor = '#51cf66'; // Greenish
                return true;
            }
        }
        return true;
    }

    // Attach listeners to Register Form
    if (registerForm) {
        const inputs = registerForm.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('input', () => validateField(input, registerForm));
            input.addEventListener('blur', () => validateField(input, registerForm));
        });

        registerForm.addEventListener('submit', function (e) {
            let isValid = true;
            inputs.forEach(input => {
                if (!validateField(input, registerForm)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
            }
        });
    }

    // Attach listeners to Login Form (only email check? Requirement said "necessary js validators for login")
    if (loginForm) {
        const inputs = loginForm.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                // Relaxed validation for login, maybe just non-empty? 
                // Or strict email validation if we want.
                // Let's apply basic checks.
                const name = input.name;
                if (name === 'email') {
                    validateField(input, loginForm);
                }
                if (name === 'password') {
                    // Just check non empty for login usually, but we can check min len
                    if (input.value.length < 1) {
                        input.style.borderColor = '#ff6b6b';
                    } else {
                        input.style.borderColor = '';
                    }
                }
            });
        });
    }
});

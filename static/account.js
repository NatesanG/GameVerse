let passIp = document.querySelector('#pass');
let p = document.querySelector('.p');
let passsIp = document.querySelector('#pass2');
let cp = document.querySelector('.cp');
let mail = document.querySelector('.mail');
let emp = document.querySelector('.emp'); // ✅ fixed bug
let names = document.querySelector('.name');
let form = document.querySelector('form');

// password validation
passIp.addEventListener('keyup', () => {
    let pass = passIp.value;
    let specialCharacter = /[@#$%&*]/; // you can expand this if needed

    if (pass !== "") {
        if (pass.length < 8 || !specialCharacter.test(pass)) {
            p.innerHTML = "Password should contain minimum 8 letters<br>including special characters";
            passIp.style.borderBottomColor = 'red';
        } else {
            p.textContent = "";
            passIp.style.borderBottomColor = 'green';
        }
    } else {
        passIp.style.borderBottomColor = 'grey';
        p.textContent = "";
    }
});

// confirm password
passsIp.addEventListener('keyup', () => {
    let pass = passIp.value;
    let passs = passsIp.value;

    if (passs === "") {
        cp.textContent = "";
        passsIp.style.borderBottomColor = 'grey';
    } else if (passs !== pass) {
        cp.textContent = "Passwords do not match";
        passsIp.style.borderBottomColor = 'red';
    } else {
        cp.textContent = "";
        passsIp.style.borderBottomColor = 'green';
    }
});

// email validation
mail.addEventListener('keyup', () => {
    let email = mail.value;
    let spCh = /^[a-zA-Z0-9._%+-]+@gmail\.com$/; // restrict to Gmail

    if (email !== "") {
        if (!spCh.test(email)) {
            emp.textContent = "Invalid Email Address";
            mail.style.borderBottomColor = 'red';
        } else {
            emp.textContent = "";
            mail.style.borderBottomColor = 'green';
        }
    } else {
        mail.style.borderBottomColor = 'grey';
        emp.textContent = "";
    }
});

// name validation
names.addEventListener('keyup', () => {
    let n = names.value;
    if (n !== "") {
        names.style.borderBottomColor = 'green';
    } else {
        names.style.borderBottomColor = 'grey';
    }
});

// final form submission check
form.addEventListener('submit', (e) => {
    if (p.textContent || cp.textContent || emp.textContent || names.value === "") {
        e.preventDefault();
        alert("Please check your credentials");
    }
});

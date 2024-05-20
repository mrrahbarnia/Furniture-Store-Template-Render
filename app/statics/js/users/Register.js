const $ = document

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const formElem = $.querySelector('.form')
const registerResult = $.querySelector('.result')
const buttons = $.querySelector('.buttons')


formElem.addEventListener('submit', (event) => {
    event.preventDefault();

    if (emailRegex.test(event.target.email.value) &&
     event.target.password.value.length >= 8 && 
     event.target.password.value == event.target.password2.value) {
        registerFetch(event.target.email.value, event.target.password.value, event.target.password2.value)
        event.target.email.value = ''
        event.target.password.value = ''
        event.target.password2.value = ''
    } else {
        registerResult.style.color = '#FFCDD2'
        registerResult.innerHTML = 'فرمت اطلاعات وارد شده صحیح نمیباشد'
    }
})

const registerFetch = async (email, password, password2) => {
    let fetchedData = await fetch('/accounts/api/v1/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'email': email, 'password': password, 'password1': password2})
    })
    if (fetchedData.status === 201) {
        registerResult.style.color = '#C8E6C9'
        registerResult.innerHTML = 'با موفقیت ثبت نام شدید'
    } else {
        let fetchedJson = await fetchedData.json()
        if (fetchedJson['extra']['fields']['email'][0] === 'Base user with this Email address already exists.') {
            registerResult.style.color = '#FFCDD2'
            registerResult.innerHTML = 'با این ایمیل قبلا ثبت نام شده است'
            buttons.insertAdjacentHTML('beforeend', 
            `
            <button class="btn" type="button" onclick="forgotBtnHandler()">فراموشی رمز عبور</button>
            `
        )
        }

    }
}

const forgotBtnHandler = () => {
    location.href = '/users/reset-password/'
}
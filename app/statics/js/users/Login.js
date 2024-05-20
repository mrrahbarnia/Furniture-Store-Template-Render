const $ = document

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const loginForm = $.querySelector('.form')
const loginResult = $.querySelector('.result')
const buttons = $.querySelector('.buttons')
const forgotBtn = $.querySelector('#forgot-btn')

loginForm.addEventListener('submit', (event) => {
    event.preventDefault();

    if (emailRegex.test(event.target.email.value) && event.target.password.value.length >= 8) {
        loginFetch(event.target.email.value, event.target.password.value)
        event.target.email.value = ''
        event.target.password.value = ''
    } else {
        loginResult.style.color = '#FFCDD2'
        loginResult.innerHTML = 'فرمت اطلاعات وارد شده صحیح نمیباشد'
    }
})

const loginFetch = async (email, password) => {
    let fetchedData = await fetch('/accounts/api/v1/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'email': email, 'password': password})
    })
    let fetchedJson = await fetchedData.json()
    if (fetchedData.status === 200) {
        setTokenToLocal(JSON.stringify({'access': fetchedJson['access'], 'refresh': fetchedJson['refresh']}))
        loginResult.style.color = '#C8E6C9'
        loginResult.innerHTML = 'با موفقیت وارد شدید'
    } else if (fetchedJson.message === 'No active account found with the given credentials') {
        loginResult.style.color = '#FFCDD2'
        loginResult.innerHTML = 'کاربری با اطلاعات وارد شده یافت نشد'
        buttons.insertAdjacentHTML('beforeend', 
            `
            <button class="btn">ثبت نام</button>
            `
        )
    }
}

const setTokenToLocal = (tokens) => {
    localStorage.setItem('AUTH-TOKEN', tokens)
}

forgotBtn.addEventListener('click', () => {
    location.href = '/users/reset-password/'
})
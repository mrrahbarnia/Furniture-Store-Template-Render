const $ = document

const formElem = $.querySelector('.form')
const verifyPasswordResult = $.querySelector('.result')
const buttons = $.querySelector('.buttons')


formElem.addEventListener('submit', (event) => {
    event.preventDefault();
    fetchVerifyPassword(event.target.password.value)
    event.target.password.value = ''
})

const fetchVerifyPassword = async(randomPassword) => {
    let fetchedData = await fetch('/accounts/api/v1/verify-password/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'rand_password': randomPassword})
    })
    let fetchedJson = await fetchedData.json()
    if (fetchedData.status === 200) {
        verifyPasswordResult.style.color = '#C8E6C9'
        verifyPasswordResult.innerHTML = `رمز عبور با موفقیت تغییر کرد<br>میتوانید رمز دلخواه خود رو بگذارید`
        buttons.insertAdjacentHTML('beforeend',
            `<button class="btn" type="button" onclick="changePasswordHandler()">رمز دلخواه</button>`
        )
    } else {
        if (fetchedJson['message'] === 'The provided password is wrong or the time limit has been expired.') {
            verifyPasswordResult.style.color = '#FFCDD2'
            verifyPasswordResult.innerHTML = 'اطلاعات وارد شده صحیح نمیباشد'
        }
    }
}

const changePasswordHandler = () => {
    location.href = '/users/change-password/'
}
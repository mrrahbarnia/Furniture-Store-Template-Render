import { refreshToken } from "./RefreshToken.js"

const $ = document

const formElem = $.querySelector('.form')
const changePasswordResult = $.querySelector('.result')
const inputsWrapper = $.querySelectorAll('.inputs-wrapper')
const firstBtn = $.querySelector('#first-btn')
const buttons = $.querySelector('.buttons')

window.addEventListener('load', () => {
    const authToken = localStorage.getItem('AUTH-TOKEN')

    if (!authToken) {
        inputsWrapper.forEach((input) => {
            input.style.display = 'none'
        })
        changePasswordResult.style.color = '#FFCDD2'
        changePasswordResult.innerHTML = 'ابتدا باید وارد شوید'
        firstBtn.innerHTML = 'ورود'
        firstBtn.addEventListener('click', (event) => {
            event.preventDefault();
            location.href = '/users/login/'
        })
    }
})

formElem.addEventListener('submit', (event) => {
    event.preventDefault();

    if (event.target['new-password'].value !== event.target['new-password2'].value) {
        changePasswordResult.innerHTML = 'رمز های جدید یکسان نمیباشند'
    } else if (event.target['new-password'].value.length < 8) {
        changePasswordResult.innerHTML = 'رمز عبور جدید باید بیشتر از هشت حرف باشد'
    } else {
        changePasswordFetch(
            event.target['old-password'].value, event.target['new-password'].value, event.target['new-password2'].value
        )
        event.target['old-password'].value = ''
        event.target['new-password'].value = ''
        event.target['new-password2'].value = ''
    }
})

const changePasswordFetch = async(oldPassword, newPassword, newPassword1) => {
    let fetchedData = await fetch('/accounts/api/v1/change-password/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getTokenFromLocal()}`
        },
        body: JSON.stringify(
            {'old_password': oldPassword, 'new_password': newPassword, 'new_password1': newPassword1}
        )
    })
    let fetchedJson = await fetchedData.json()
    if (fetchedData.status === 200) {
        changePasswordResult.style.color = '#C8E6C9'
        changePasswordResult.innerHTML = 'رمز عبور با موفقیت تغییر یافت'
    } else if (fetchedJson['message']['code'] === 'token_not_valid') {
        refreshToken(
            changePasswordFetch(
                oldPassword, newPassword, newPassword1
            )
        );
    }
}

const getTokenFromLocal = () => JSON.parse(localStorage.getItem('AUTH-TOKEN'))['access']
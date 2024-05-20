const $ = document

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const resetPasswordForm = $.querySelector('.form')
const resetPasswordResult = $.querySelector('.result')
const buttons = $.querySelector('.buttons')

resetPasswordForm.addEventListener('submit', (event) => {
    event.preventDefault();

    if (emailRegex.test(event.target.email.value)) {
        resetPasswordFetch(event.target.email.value)
        event.target.email.value = ''
    } else {
        resetPasswordResult.style.color = '#FFCDD2'
        resetPasswordResult.innerHTML = 'فرمت ایمیل صحیح نمیباشد'
        event.target.email.value = ''
        buttons.insertAdjacentHTML('beforeend', 
            `
            <button class='btn' type='button' onclick="showEmailFormatHandler(event)">مشاهده فرمت صحیح</button>
            `
        )
    }
})
const showEmailFormatHandler = (event) => {
    event.preventDefault();
    resetPasswordResult.style.color = '#fff'
    resetPasswordResult.innerHTML = 'Example@example.com'
}

const resetPasswordFetch = async(email) => {
    let fetchedData = await fetch('/accounts/api/v1/reset-password/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'email': email})
    })
    let fetchedJson = await fetchedData.json()
    if (fetchedData.status === 200) {
        const succeedMessage = fetchedJson['message']
        let totalSeconds = succeedMessage.match(/(\d+)/);
        if (totalSeconds) {
            resetPasswordResult.style.color = '#C8E6C9'
            resetPasswordResult.innerHTML = `لینک بازیابی با انقضای ${totalSeconds[0]} ثانیه برای شما ارسال شد`
        }

    } else {
        if (fetchedJson['message'] === 'Validation Error') {
            resetPasswordResult.style.color = '#FFCDD2'
            resetPasswordResult.innerHTML = 'ایمیل وارد شده از قبل ثبت نشده است'
        }
    }
}
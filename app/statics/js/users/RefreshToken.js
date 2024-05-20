const refreshToken = async(callback) => {
    console.log('Refresh token function called...');
    const refreshToken = JSON.parse(localStorage.getItem('AUTH-TOKEN'))['refresh']
    let fetchedData = await fetch('/accounts/api/v1/refresh/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'refresh': refreshToken})
    })
    let fetchedJson = await fetchedData.json()
    if (fetchedData.status === 200) {
        console.log('Replaced');
        localStorage.setItem('AUTH-TOKEN', JSON.stringify({'access': fetchedJson['access'], 'refresh': fetchedJson['refresh']}))
        callback(...args)
    } else {
        location.href = '/users/login/'
    }
}

export { refreshToken };
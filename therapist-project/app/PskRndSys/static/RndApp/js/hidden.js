// şifreyi görünür/gizli olarak değiştirir
const passwordEle = document.getElementById('password');
const toggleEle = document.getElementById('toggle');

// click eventini dinliyor ve şifreyi görünür/gizli olarak değişiriyor
toggleEle.addEventListener('click', function () {
    const type = passwordEle.getAttribute('type');

    passwordEle.setAttribute(
        'type',

        type === 'password' ? 'text' : 'password'
    );
});
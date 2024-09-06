// JavaScript to handle basic interactivity
document.addEventListener('DOMContentLoaded', function() {
    const contactLink = document.querySelector('#contact a');

    contactLink.addEventListener('click', function(event) {
        event.preventDefault();
        alert('You clicked the contact link! Send me an email at: sandeepsai660@gmail.com');
    });
});
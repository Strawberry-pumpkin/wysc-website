// carousel for accomodation at index.html
function carouselchange(num){
    const elems=document.querySelectorAll("#carousel div")
    console.log(elems)
      for (let i=0;i<elems.length;i++){
      elems[i].style.opacity='0'
      }
      elems[num].style.opacity='100%'

  }

  window.onload = (event) => {
    i=0
  setInterval(() => {
    carouselchange(i)
    i+=1;
    if (i>2){
      i=0
    }
  }, 5000);
};



// navbar of wysc.html
window.addEventListener('scroll', () => {
const navbar = document.getElementById('navbar');
if (window.scrollY > 0) {

navbar.classList.replace('text-white','text-black')
navbar.classList.add('shadow-md')
navbar.classList.add('backdrop-blur-sm')

} else {

navbar.classList.replace('text-black','text-white')
navbar.classList.remove('shadow-md')
navbar.classList.add('backdrop-blur-sm')
}
});

// responsive navbar for both
const menuBtn = document.getElementById('menuBtn');
const menu = document.getElementById('menu');

menuBtn.addEventListener('click', () => {
    menu.classList.toggle('hidden');
    if (menuBtn.name=='menu'){
        menuBtn.name='close'
    }
    else{
        menuBtn.name = 'menu'
    }
});

// reveal sets of 4 images for gallery at wysc.html
max_im = 8
// no of max images available for the gallery (minus 8 for the defaults)
// first image goes as wysc-0
current_count = 7
function reveal(){
    if (max_im-current_count*4>=4){
        // wont load images unless theres a set of 4 images available
        let gallery = document.getElementById('gallery');
    
        let columns = (gallery.childNodes[3].children)
        for (let i=0; i<columns.length; i+=1){
            const div = document.createElement('div');
        const img = document.createElement('img');
    
        img.src = `/static/images/gallery/wysc-${current_count*4+i}.jpg`;
        // current count = no of rows,
        // multiply by four to skip four images in the urls list
        img.classList.add('rounded-md')
        img.classList.add('h-auto')
        img.classList.add('max-w-full')
        
        
        div.appendChild(img)
            columns[i].appendChild(div)
    
    }
   

    }
    current_count+=1
}

// countdown for wysc.html
function countdown() {
    const endDate = new Date("Sep 06, 2024 23:59:59").getTime();
    const now = new Date().getTime();
    const timeLeft = endDate - now;

    const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

    if (days<10){
    document.getElementById("days").innerText = '0' + days;
    }
    else{
        document.getElementById("days").innerText =  days;
    }
    if (hours<10){
    document.getElementById("hours").innerText = '0' + hours;
    }
    else{
        document.getElementById("hours").innerText =  hours;
    }
    if (minutes<10){
    document.getElementById("minutes").innerText = '0' + minutes;
    }
    else{
        document.getElementById("minutes").innerText =  minutes;
    }
    if (seconds<10){
    document.getElementById("seconds").innerText = '0' + seconds;
    }
    else{
        document.getElementById("seconds").innerText =  seconds;
    }
    if (timeLeft < 0) {
        clearInterval(timer);
        document.getElementById("days").innerText = "0";
        document.getElementById("hours").innerText = "0";
        document.getElementById("minutes").innerText = "0";
        document.getElementById("seconds").innerText = "0";
    }
}

const timer = setInterval(countdown, 1000);

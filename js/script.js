let slideCart = document.getElementById('slide-cart'); //container

function scrollLeft(event){
    event.preventDefault(); //disable scroll on the page

    //velocity sum: sign * sqrt(x**2 + y**2)
    delta = event.deltaX**2 + event.deltaY**2;
    sign = Math.sign(event.deltaX + event.deltaY);
    delta = sign * Math.sqrt(delta);
    
    event.currentTarget.scrollLeft += delta; //keep x-axis scroll (trackpad/touchscreen). Sum x velocity and y velocity (vectors)
}

slideCart.addEventListener('wheel', scrollLeft);
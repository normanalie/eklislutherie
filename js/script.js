let slideCart = document.getElementById('slide-cart'); //container

function scrollLeft(event){
    maxScrollLeft = event.currentTarget.scrollWidth - event.currentTarget.clientWidth;

    //velocity sum: sign * sqrt(x**2 + y**2)
    delta = event.deltaX**2 + event.deltaY**2;
    sign = Math.sign(event.deltaX + event.deltaY);
    delta = sign * Math.sqrt(delta);
    
    //resumes its normal behavior at the beginning and end of the block
    if( (sign > 0 && event.currentTarget.scrollLeft < maxScrollLeft) || (sign < 0 && event.currentTarget.scrollLeft > 0) ){ //(scroll to bottom and not at the end of the block) or (scroll to top and not a the start of the block)
        event.preventDefault();
        event.currentTarget.scrollLeft += delta; //keep x-axis scroll (trackpad/touchscreen). Sum x velocity and y velocity (vectors)
    }
}

slideCart.addEventListener('wheel', scrollLeft);
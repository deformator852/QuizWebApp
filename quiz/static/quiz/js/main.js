function main(){
    const elements = document.getElementsByClassName("choice");

    for (let i = 0; i < elements.length; i++) {
      elements[i].addEventListener("click", function(e) {
        const radioInput = elements[i].querySelector('input[type="radio"]');
        for (let j = 0; j < elements.length; j++) {
            elements[j].classList.remove("current-chose");
          }
        elements[i].classList.add("current-chose")
        if (radioInput) {
            radioInput.checked = true;
        }
      });
    }
    
}

main()
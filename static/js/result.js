export const renderResultTemplate = (result) => {
    console.log("rendering the result:", result);
    const resultTemplate = document.querySelector(".auth-result");
    let resultMessage = document.querySelector("p.auth-result-msg");
  
    resultMessage.innerHTML = `${result}`;
  
    resultTemplate.classList.add("show-auth-result");
  };
  
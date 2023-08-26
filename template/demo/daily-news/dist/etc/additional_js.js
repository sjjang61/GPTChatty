// # html include 방식 구현 
  function includeHTML(){
      let z, elmnt, file, xhttp;
   
      z = document.getElementsByTagName("*");
      
      for (let i = 0; i < z.length; i++) {
        elmnt = z[i];
        file = elmnt.getAttribute("data-include");
        
        if (file) {
          xhttp = new XMLHttpRequest();
          xhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
              if (this.status == 200) {elmnt.innerHTML = this.responseText;}
              if (this.status == 404) {elmnt.innerHTML = "Page not found.";}
              /* Remove the attribute, and call this function once more: */
              elmnt.removeAttribute("data-include");
              includeHTML();
            }//if
          }//onreadystatechange
   
          xhttp.open("GET", file, true);
          xhttp.send();
          return;
        }//if - file
      }//for
  }//includeHTML
   
   
  /* ✨ 실행 */
  window.addEventListener('DOMContentLoaded',()=>{
      includeHTML();
  });



// # 메뉴 활성/비활성화 처리 

// 현재 페이지의 URL을 가져오는 함수
function getCurrentPageURL() {
  return window.location.href;
}

// URL에 따라서 "active" 클래스를 추가할 요소를 결정하는 함수
function addActiveClassBasedOnURL() {
  var currentPageURL = getCurrentPageURL();
  //main menu
  if (currentPageURL.includes("/html/article.html")) {
    addActiveClassToElement("menu_article");
    showAlert("menu_article");
  } else if (currentPageURL.includes("/html/class_")) {
    addActiveClassToElement("menu_class");
    showAlert("menu_class");
  } else if (currentPageURL.includes("/html/remind.html")) {
    addActiveClassToElement("menu_remind");
    showAlert("menu_remind");
  } else if (currentPageURL.includes("/html/setting.html")) {
    addActiveClassToElement("menu_setting");
    showAlert("menu_setting");
  }  
    
  //sub menu : class
  if (currentPageURL.includes("/html/class_body.html")) {
    addActiveClassToElement("menu_class_body");
    showAlert("menu_class_body");
  } else if (currentPageURL.includes("/html/class_keyword.html")) {
    addActiveClassToElement("menu_class_keyword");
    showAlert("menu_class_keyword");
  } else if (currentPageURL.includes("/html/class_example.html")) {
    addActiveClassToElement("menu_class_example");
    showAlert("menu_class_example");
  } else if (currentPageURL.includes("/html/class_talk.html")) {
    addActiveClassToElement("menu_class_talk");
    showAlert("menu_class_talk");
  }

}

// 특정 HTML 요소에 "active" 클래스를 추가하는 함수
function addActiveClassToElement(elementId) {
  var element = document.getElementById(elementId);
  if (element) {
    element.classList.add("active");
    element.classList.remove("link-dark"); // 기존의 "line-dark" 클래스 제거
  }
}

// 선택된 ID와 현재 페이지 URL, 클래스 목록을 얼럿으로 표시하는 함수
function showAlert(selectedId) {
  var currentPageURL = getCurrentPageURL();
  var element = document.getElementById(selectedId);
  var classList = element ? Array.from(element.classList).join(", ") : "No class";

  //alert("현재 페이지 URL: " + currentPageURL + "\n선택된 ID: " + selectedId + "\n클래스 목록: " + classList);
}

// 페이지 로드가 모두 끝나고 window.onload 이벤트가 발생했을 때, 2초 후에 URL에 따라 "active" 클래스를 추가하고 선택된 ID와 현재 URL을 얼럿으로 표시
window.onload = function () {
  setTimeout(function() {
    addActiveClassBasedOnURL();
  }, 500); // 2초(2000ms) 딜레이
};
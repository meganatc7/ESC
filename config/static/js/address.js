function DaumPostcode() {
  new daum.Postcode({
      oncomplete: function(data) {
          var addr = data.address; // 최종 주소 변수

          //주소 정보를 해당 인풋 필드에 받아옴
          document.getElementById("address").value = addr;
      }
  }).open();
} 
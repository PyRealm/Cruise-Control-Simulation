function setActive(button) {
    let buttons = document.querySelectorAll('.car-type-buttons button');
    buttons.forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
    document.getElementById('car_type').value = button.value;
  }
  
  window.onload = function() {
    {% if v0 %}
    document.querySelector('input[name="v0"]').value = {{ v0 }};
    document.querySelector('output[name="v0_out"]').value = {{ v0 }};
    {% endif %}
  
    {% if v_set %}
    document.querySelector('input[name="v_set"]').value = {{ v_set }};
    document.querySelector('output[name="v_set_out"]').value = {{ v_set }};
    {% endif %}
  
    {% if Tp %}
    document.querySelector('input[name="Tp"]').value = {{ Tp }};
    document.querySelector('output[name="Tp_out"]').value = {{ Tp }};
    {% endif %}
  
    {% if Ti %}
    document.querySelector('input[name="Ti"]').value = {{ Ti }};
    document.querySelector('output[name="Ti_out"]').value = {{ Ti }};
    {% endif %}
  
    {% if Td %}
    document.querySelector('input[name="Td"]').value = {{ Td }};
    document.querySelector('output[name="Td_out"]').value = {{ Td }};
    {% endif %}
  
    {% if theta %}
    document.querySelector('input[name="theta"]').value = {{ theta }};
    document.querySelector('output[name="theta_out"]').value = {{ theta }};
    {% endif %}
  
    {% if kp %}
    document.querySelector('input[name="kp"]').value = {{ kp }};
    document.querySelector('output[name="kp_out"]').value = {{ kp }};
    {% endif %}
  };
  
document.querySelector('form').addEventListener('submit', function(event) {
  event.preventDefault();

  const inputDate = document.querySelector('#data');
  const inputTime = document.querySelector('#hora');
  const inputName = document.querySelector('#name');
  const alarmAudio = document.querySelector('#alarme');

  // Adicionando referências aos novos elementos
  const customAlert = document.querySelector('#custom-alert');
  const alertMessage = document.querySelector('#alert-message');
  const alertOkButton = document.querySelector('#alert-ok');

  const reminderDateTimeString = `${inputDate.value}T${inputTime.value}:00`;
  const reminderDateTime = new Date(reminderDateTimeString);
  const now = new Date();
  const timeDifference = reminderDateTime.getTime() - now.getTime();

  if (timeDifference > 0) {
    console.log(`Lembrete "${inputName.value}" agendado para ${reminderDateTime}.`);
    
    setTimeout(() => {
      // 1. Toca o áudio imediatamente
      alarmAudio.play();
      
      // 2. Exibe a caixa de notificação
      alertMessage.textContent = `🔔 Lembrete: ${inputName.value}\nÉ hora de bater o ponto!`;
      customAlert.style.display = 'block';

    }, timeDifference);
    
    document.querySelector('form').reset();
  } else {
    alert('Por favor, selecione uma data e hora no futuro.');
  }

  // Evento para fechar a notificação quando o botão OK for clicado
  alertOkButton.addEventListener('click', () => {
    customAlert.style.display = 'none';
  });
});

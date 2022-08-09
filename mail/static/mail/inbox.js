document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email('Nothing'));

  // By default, load the inbox
  load_mailbox('inbox');

  
});

function archive_email(mailID, archive) {
  fetch(`/emails/${mailID}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: archive
    })
  });

  location.reload();
}

function read_email(mailID, mailbox) {

  // Show read view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'block';

  // Mark email as read
  fetch(`/emails/${mailID}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });

  // Get the email according to id
  fetch(`/emails/${mailID}`)
  .then(response => response.json())
  .then(email => {

    // Print email
    console.log(email);

    // Fill email info into html
    document.querySelector('#read-sender').innerHTML = email.sender;
    document.querySelector('#read-recipients').innerHTML = email.recipients;
    document.querySelector('#read-timestamp').innerHTML = email.timestamp;
    document.querySelector('#read-subject').innerHTML = email.subject;

    // Convert new line
    content = email.body;
    document.querySelector('#content').innerHTML = content.replaceAll('\n', '<br/>');
      
    // Unhide the archive button
    document.querySelector('#read-archive').hidden = false;

    // Listen to reply button onclick
    document.querySelector('#read-reply').addEventListener('click', () => compose_email(email));

    // Check mailbox
    if (mailbox === 'inbox') {
      
      document.querySelector('#read-archive').innerHTML = 'Archive';

      document.querySelector('#read-archive').addEventListener('click', () => archive_email(mailID, true));

    } else if (mailbox === 'archive') {

      document.querySelector('#read-archive').innerHTML = 'Unarchive';

      document.querySelector('#read-archive').addEventListener('click', () => archive_email(mailID, false));

    } else {document.querySelector('#read-archive').hidden = true;}
  });

  return false;
}

function compose_email(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Check for replying 
  if (email !== 'Nothing') {
    
    // Prefill recipient
    document.querySelector('#compose-recipients').value = email.sender;

    // Prefill subject
    if (email.subject.substr(0, 4) !== 'Re: ') {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    } else {document.querySelector('#compose-subject').value = email.subject;}

    // Prefill email body
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
  } else {}

  // Listen for submittion of email composing
  document.querySelector('#compose-form').onsubmit = () => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);

        // Verify message
        if (result.error) {
          alert(result.error);
        } else {
          alert(result.message);
          load_mailbox('sent');
        }
        
    });

    // Stop from submitting
    return false;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get mails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    // Print emails
    console.log(emails);

    // Iterate array
    emails.forEach(email => {
    
      // Create email card
      const element = document.createElement('div');
      element.class = 'card';
      element.innerHTML = `<div class="card-body">\n
      <h5 class="card-title">${email.subject}</h5>\n
      <p class="card-text">By ${email.sender} at ${email.timestamp}</p>\n
      </div>`;

      // Style
      element.style.border = "thin solid blue";
      element.style.marginTop = "20px";
      element.style.marginBottom = "20px";
      element.style.borderRadius = "10px";

      if (email.read === true) {
        element.style.backgroundColor = "gray";
      } else {}

      // Implement behaviour onclick
      element.addEventListener('click', () => read_email(email.id, mailbox));

      // Append mail card
      document.querySelector('#emails-view').append(element);
    });
    
  });
}
document.addEventListener('DOMContentLoaded', function(){
  const avatarInput = document.querySelector('input[type=file][name=avatar_file]');
  const avatarPreview = document.getElementById('avatarPreview');
  if(avatarInput && avatarPreview){
    avatarInput.addEventListener('change', function(e){
      const f = this.files && this.files[0];
      if(!f){ avatarPreview.classList.add('d-none'); avatarPreview.src = ''; return; }
      const url = URL.createObjectURL(f);
      avatarPreview.src = url; avatarPreview.classList.remove('d-none');
    });
  }

  const mediaInput = document.querySelector('input[type=file][name=media_files]');
  const mediaPreview = document.getElementById('mediaPreview');
  if(mediaInput && mediaPreview){
    mediaInput.addEventListener('change', function(e){
      mediaPreview.innerHTML = '';
      Array.from(this.files).forEach(f => {
        const type = f.type || '';
        if(type.startsWith('image/')){
          const img = document.createElement('img');
          img.src = URL.createObjectURL(f);
          img.className = 'rounded';
          mediaPreview.appendChild(img);
        } else if(type.startsWith('video/')){
          const vid = document.createElement('video');
          vid.src = URL.createObjectURL(f);
          vid.controls = true;
          vid.className = 'rounded';
          vid.style.maxWidth = '200px';
          mediaPreview.appendChild(vid);
        }
      });
    });
  }
});

// FilePond initialization (if library loaded)
if(window.FilePond){
  // Turn all file inputs into FilePond instances with default settings
  FilePond.parse(document.body);
  // Example: set options globally
  FilePond.setOptions({
    allowMultiple: true,
    instantUpload: false,
  });
}

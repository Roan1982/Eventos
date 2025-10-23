document.addEventListener('DOMContentLoaded', function(){
  // ===== Select2 Init for all select elements =====
  if(typeof $ !== 'undefined' && $.fn.select2){
    // Initialize Select2 for all select inputs
    $('select').each(function(){
      $(this).select2({
        theme: 'bootstrap-5',
        width: '100%',
        placeholder: $(this).attr('data-placeholder') || 'Seleccionar...',
        allowClear: !$(this).prop('required'),
        language: {
          noResults: function() { return "No hay resultados"; },
          searching: function() { return "Buscando..."; }
        }
      });
    });
  }

  // ===== Avatar Preview =====
  const avatarInput = document.querySelector('input[type=file][name=avatar_file]');
  const avatarPreview = document.getElementById('avatarPreview');
  if(avatarInput && avatarPreview){
    avatarInput.addEventListener('change', function(e){
      const f = this.files && this.files[0];
      if(!f){ 
        if(avatarPreview.classList) avatarPreview.classList.add('d-none'); 
        avatarPreview.src = ''; 
        return; 
      }
      const url = URL.createObjectURL(f);
      avatarPreview.src = url; 
      if(avatarPreview.classList) avatarPreview.classList.remove('d-none');
    });
  }

  // ===== FilePond Configuration =====
  console.log('Checking FilePond...', window.FilePond ? 'LOADED' : 'NOT LOADED');
  if(window.FilePond){
    // Register plugins
    if(window.FilePondPluginFileValidateType) FilePond.registerPlugin(FilePondPluginFileValidateType);
    if(window.FilePondPluginFileValidateSize) FilePond.registerPlugin(FilePondPluginFileValidateSize);
    if(window.FilePondPluginImagePreview) FilePond.registerPlugin(FilePondPluginImagePreview);
    if(window.FilePondPluginImageExifOrientation) FilePond.registerPlugin(FilePondPluginImageExifOrientation);

    // Initialize FilePond for media_files input
    const mediaInput = document.querySelector('input[type=file][name=media_files]');
    console.log('Media input found:', mediaInput ? 'YES' : 'NO');
    if(mediaInput){
      console.log('Initializing FilePond...');
      
      const pond = FilePond.create(mediaInput, {
        allowMultiple: true,
        instantUpload: false,
        storeAsFile: true,
        maxFileSize: '10MB',
        acceptedFileTypes: ['image/*', 'video/*'],
        maxFiles: 10,
        name: 'media_files',
        allowReorder: true,
        credits: false,
        // Image Preview settings
        allowImagePreview: true,
        imagePreviewHeight: 170,
        imagePreviewMaxHeight: 256,
        imagePreviewMinHeight: 100,
        imagePreviewMaxFileSize: '10MB',
        imagePreviewTransparencyIndicator: 'grid',
        labelIdle: `
          <div class="filepond-label-wrapper">
            <i class="fas fa-cloud-upload-alt fa-3x mb-2"></i>
            <p class="mb-1"><strong>Arrastra y suelta tus archivos aquí</strong></p>
            <p class="small text-muted">o haz clic para seleccionar</p>
            <p class="small text-muted">Imágenes y videos (Max 10MB cada uno)</p>
          </div>
        `,
        labelFileProcessing: 'Procesando',
        labelFileProcessingComplete: 'Listo',
        labelTapToCancel: 'Clic para cancelar',
        labelTapToRetry: 'Clic para reintentar',
        labelTapToUndo: 'Clic para deshacer',
        labelButtonRemoveItem: 'Eliminar',
        labelButtonAbortItemLoad: 'Cancelar',
        labelButtonRetryItemLoad: 'Reintentar',
        labelButtonAbortItemProcessing: 'Cancelar',
        labelButtonUndoItemProcessing: 'Deshacer',
        labelButtonRetryItemProcessing: 'Reintentar',
        labelButtonProcessItem: 'Subir',
        labelMaxFileSizeExceeded: 'Archivo muy grande',
        labelMaxFileSize: 'Tamaño máximo: {filesize}',
        labelFileTypeNotAllowed: 'Tipo de archivo no permitido',
        fileValidateTypeLabelExpectedTypes: 'Espera {allButLastType} o {lastType}',
        stylePanelLayout: 'compact',
        styleLoadIndicatorPosition: 'center bottom',
        styleProgressIndicatorPosition: 'right bottom',
        styleButtonRemoveItemPosition: 'left bottom',
        styleButtonProcessItemPosition: 'right bottom',
      });
      
      console.log('FilePond initialized successfully with image preview');
    }
  }

  // ===== Hover Actions for Existing Media (Edit Form) =====
  const mediaCards = document.querySelectorAll('.media-card-edit');
  mediaCards.forEach(card => {
    const deleteCheckbox = card.querySelector('input[type=checkbox][name=delete_media]');
    const coverRadio = card.querySelector('input[type=radio][name=cover_media]');
    
    // Create hover overlay
    const overlay = document.createElement('div');
    overlay.className = 'media-hover-overlay';
    overlay.innerHTML = `
      <div class="media-hover-actions">
        <button type="button" class="btn btn-danger btn-sm hover-delete-btn" title="Eliminar">
          <i class="fas fa-trash"></i>
        </button>
        <button type="button" class="btn btn-warning btn-sm hover-cover-btn" title="Portada">
          <i class="fas fa-star"></i>
        </button>
      </div>
    `;
    
    card.querySelector('.media-preview').appendChild(overlay);
    
    // Handle delete button click
    const deleteBtn = overlay.querySelector('.hover-delete-btn');
    deleteBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if(deleteCheckbox){
        deleteCheckbox.checked = !deleteCheckbox.checked;
        if(deleteCheckbox.checked){
          card.style.opacity = '0.5';
          card.style.border = '2px solid #dc3545';
          deleteBtn.innerHTML = '<i class="fas fa-undo"></i>';
          deleteBtn.classList.remove('btn-danger');
          deleteBtn.classList.add('btn-secondary');
          deleteBtn.title = 'Cancelar eliminación';
        } else {
          card.style.opacity = '1';
          card.style.border = '2px solid var(--border-color)';
          deleteBtn.innerHTML = '<i class="fas fa-trash"></i>';
          deleteBtn.classList.remove('btn-secondary');
          deleteBtn.classList.add('btn-danger');
          deleteBtn.title = 'Eliminar';
        }
      }
    });
    
    // Handle cover button click
    const coverBtn = overlay.querySelector('.hover-cover-btn');
    coverBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if(coverRadio){
        coverRadio.checked = true;
        // Update all cards to show which is cover
        document.querySelectorAll('.media-card-edit').forEach(c => {
          c.classList.remove('is-cover');
        });
        card.classList.add('is-cover');
      }
    });
    
    // Check initial state
    if(deleteCheckbox && deleteCheckbox.checked){
      card.style.opacity = '0.5';
      card.style.border = '2px solid #dc3545';
    }
    if(coverRadio && coverRadio.checked){
      card.classList.add('is-cover');
    }
  });

  // ===== Gallery / Carousel Init =====
  function initGallery(gallery){
    if(!gallery) return;
    try{
      const media = JSON.parse(gallery.getAttribute('data-media') || '[]');
      if(!media.length) return;
      
      let index = 0;
      const wrapper = document.getElementById('mainMediaWrapper');
      
      const renderSlot = (pos, item) => {
        const slot = gallery.querySelector('.thumb-slot[data-pos="'+pos+'"]');
        if(!slot) return; 
        slot.innerHTML = '';
        if(!item) return;
        
        if(item.mime === 'image'){
          const img = document.createElement('img'); 
          img.src = item.url; 
          img.className='img-fluid rounded'; 
          img.style.height='100px'; 
          img.style.objectFit='cover'; 
          img.style.width='100%'; 
          img.style.cursor='pointer';
          slot.appendChild(img);
        } else if(item.mime === 'video'){
          const vid = document.createElement('video'); 
          vid.muted=true; 
          vid.className='w-100 rounded'; 
          vid.style.height='100px';
          vid.style.objectFit='cover';
          vid.style.cursor='pointer';
          const s=document.createElement('source'); 
          s.src=item.url; 
          s.type=item.ctype; 
          vid.appendChild(s); 
          slot.appendChild(vid);
        } else { 
          slot.textContent = item.filename; 
        }
      };
      
      const renderMain = (item) => {
        if(!wrapper) return; 
        wrapper.innerHTML = '';
        if(!item) return;
        
        if(item.mime === 'image'){
          const img = document.createElement('img'); 
          img.id='mainMedia'; 
          img.src=item.url; 
          img.className='img-fluid rounded'; 
          img.style.maxHeight='400px'; 
          img.style.objectFit='contain'; 
          img.style.width='100%';
          wrapper.appendChild(img);
        } else if(item.mime === 'video'){
          const vid = document.createElement('video'); 
          vid.controls=true; 
          vid.id='mainMedia'; 
          vid.className='w-100 rounded'; 
          vid.style.maxHeight='400px'; 
          vid.style.objectFit='contain'; 
          const s=document.createElement('source'); 
          s.src=item.url; 
          s.type=item.ctype; 
          vid.appendChild(s); 
          wrapper.appendChild(vid);
        } else { 
          const a=document.createElement('a'); 
          a.id='mainMedia'; 
          a.href=item.url; 
          a.textContent=item.filename; 
          wrapper.appendChild(a); 
        }
      };
      
      const update = () => {
        const prev = media[(index-1+media.length)%media.length];
        const curr = media[index];
        const next = media[(index+1)%media.length];
        renderSlot('prev', prev); 
        renderSlot('current', curr); 
        renderSlot('next', next); 
        renderMain(curr);
      };
      
      const prevBtn = document.getElementById('prevBtn');
      const nextBtn = document.getElementById('nextBtn');
      if(prevBtn) prevBtn.addEventListener('click', ()=>{ 
        index = (index-1+media.length)%media.length; 
        update(); 
      });
      if(nextBtn) nextBtn.addEventListener('click', ()=>{ 
        index = (index+1)%media.length; 
        update(); 
      });
      
      gallery.addEventListener('click', function(e){
        const slot = e.target.closest('.thumb-slot'); 
        if(!slot) return; 
        const pos = slot.getAttribute('data-pos');
        if(pos === 'prev') index = (index-1+media.length)%media.length; 
        else if(pos === 'next') index = (index+1)%media.length; 
        update();
      });
      
      update();
    }catch(err){ 
      console.error('Failed to init gallery', err); 
    }
  }

  // Initialize gallery if exists
  const gallery = document.getElementById('gallery');
  if(gallery){ 
    initGallery(gallery); 
  }

  // ===== Leaflet Map for Event Location =====
  const mapElement = document.getElementById('event-map');
  if (mapElement && typeof L !== 'undefined') {
    const address = mapElement.getAttribute('data-address');
    const city = mapElement.getAttribute('data-city');
    const venue = mapElement.getAttribute('data-venue');
    
    // Construir la query para Nominatim
    const searchQuery = [address, city].filter(Boolean).join(', ');
    
    if (searchQuery) {
      // Usar Nominatim para geocodificar la dirección
      fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}&limit=1`)
        .then(response => response.json())
        .then(data => {
          if (data && data.length > 0) {
            const lat = parseFloat(data[0].lat);
            const lon = parseFloat(data[0].lon);
            
            // Crear el mapa
            const map = L.map('event-map').setView([lat, lon], 15);
            
            // Agregar capa de OpenStreetMap
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
              attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
              maxZoom: 19
            }).addTo(map);
            
            // Agregar marcador
            const markerIcon = L.icon({
              iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
              shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
              iconSize: [25, 41],
              iconAnchor: [12, 41],
              popupAnchor: [1, -34],
              shadowSize: [41, 41]
            });
            
            const marker = L.marker([lat, lon], { icon: markerIcon }).addTo(map);
            
            // Popup con información
            const popupContent = `
              <div style="text-align: center;">
                <strong>${venue || 'Ubicación del Evento'}</strong><br>
                ${address ? address + '<br>' : ''}
                ${city}<br>
                <a href="https://www.google.com/maps/dir/?api=1&destination=${lat},${lon}" 
                   target="_blank" class="btn btn-sm btn-primary mt-2">
                  <i class="fas fa-directions"></i> Cómo llegar
                </a>
              </div>
            `;
            marker.bindPopup(popupContent).openPopup();
          } else {
            // Si no se encuentra, mostrar mapa centrado en Argentina
            mapElement.innerHTML = `
              <div class="alert alert-warning mb-0">
                <i class="fas fa-exclamation-triangle"></i> 
                No se pudo geocodificar la dirección exacta. Por favor verifica la ubicación manualmente.
                <br><strong>Dirección:</strong> ${searchQuery}
              </div>
            `;
          }
        })
        .catch(error => {
          console.error('Error al geocodificar:', error);
          mapElement.innerHTML = `
            <div class="alert alert-danger mb-0">
              <i class="fas fa-times-circle"></i> 
              Error al cargar el mapa. Por favor intenta más tarde.
            </div>
          `;
        });
    } else {
      mapElement.innerHTML = `
        <div class="alert alert-info mb-0">
          <i class="fas fa-info-circle"></i> 
          No hay información de ubicación disponible para este evento.
        </div>
      `;
    }
  }

  // ===== Star Rating System =====
  const starContainers = document.querySelectorAll('.star-rating');
  starContainers.forEach(container => {
    const isInteractive = container.classList.contains('interactive');
    const ratingInput = document.getElementById('rating-value');
    const stars = container.querySelectorAll('.star');
    
    if (isInteractive && ratingInput) {
      // Interactive star rating (for form)
      let currentRating = parseFloat(ratingInput.value) || 0;
      
      const updateStars = (rating) => {
        stars.forEach((star, index) => {
          const starValue = index + 1;
          const halfValue = index + 0.5;
          
          star.classList.remove('full', 'half', 'empty');
          
          if (rating >= starValue) {
            star.classList.add('full');
          } else if (rating >= halfValue) {
            star.classList.add('half');
          } else {
            star.classList.add('empty');
          }
        });
      };
      
      stars.forEach((star, index) => {
        // Click to select full star
        star.addEventListener('click', (e) => {
          const rect = star.getBoundingClientRect();
          const clickX = e.clientX - rect.left;
          const halfWidth = rect.width / 2;
          
          // If clicked on left half, set to .5, otherwise full star
          if (clickX < halfWidth) {
            currentRating = index + 0.5;
          } else {
            currentRating = index + 1;
          }
          
          ratingInput.value = currentRating;
          updateStars(currentRating);
        });
        
        // Hover preview
        star.addEventListener('mouseenter', () => {
          updateStars(index + 1);
        });
      });
      
      container.addEventListener('mouseleave', () => {
        updateStars(currentRating);
      });
      
      // Initialize with current value
      updateStars(currentRating);
    } else {
      // Display-only star rating
      const rating = parseFloat(container.getAttribute('data-rating')) || 0;
      stars.forEach((star, index) => {
        const starValue = index + 1;
        const halfValue = index + 0.5;
        
        star.classList.remove('full', 'half', 'empty');
        
        if (rating >= starValue) {
          star.classList.add('full');
        } else if (rating >= halfValue) {
          star.classList.add('half');
        } else {
          star.classList.add('empty');
        }
      });
    }
  });
});

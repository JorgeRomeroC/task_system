// Configuración global de SweetAlert2
const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
});

// Confirmación para eliminar tarea
function confirmDelete(taskId, taskTitle) {
    Swal.fire({
        title: '¿Eliminar tarea?',
        html: `<p class="text-gray-600">¿Estás seguro de eliminar la tarea:</p><p class="font-semibold mt-2">"${taskTitle}"</p>`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ef4444',
        cancelButtonColor: '#6b7280',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            // Detectar si estamos en el dashboard o en la vista normal
            const isDashboard = window.location.pathname.includes('/dashboard');
            const deleteUrl = isDashboard 
                ? `/tasks/dashboard/task/${taskId}/delete/`
                : `/tasks/${taskId}/delete/`;
            
            // Ejecutar la petición DELETE con HTMX
            const taskElement = document.getElementById(`task-${taskId}`);
            htmx.ajax('DELETE', deleteUrl, {
                target: `#task-${taskId}`,
                swap: 'outerHTML'
            }).then(() => {
                Toast.fire({
                    icon: 'success',
                    title: 'Tarea eliminada correctamente'
                });
            });
        }
    });
    return false;
}

// Confirmación para cerrar sesión
function confirmLogout(event) {
    event.preventDefault();
    Swal.fire({
        title: '¿Cerrar sesión?',
        text: '¿Estás seguro de que deseas cerrar tu sesión?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3b82f6',
        cancelButtonColor: '#6b7280',
        confirmButtonText: 'Sí, cerrar sesión',
        cancelButtonText: 'Cancelar',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/logout/';
        }
    });
}

// Alerta de éxito al crear tarea
function taskCreated() {
    Toast.fire({
        icon: 'success',
        title: 'Tarea creada exitosamente'
    });
}

// Alerta de éxito al actualizar tarea
function taskUpdated() {
    Toast.fire({
        icon: 'success',
        title: 'Tarea actualizada correctamente'
    });
}

// Alerta de éxito al completar/descompletar tarea
function taskToggled(completed) {
    Toast.fire({
        icon: 'success',
        title: completed ? 'Tarea completada' : 'Tarea marcada como pendiente'
    });
}

// Alerta de error genérica
function showError(message) {
    Toast.fire({
        icon: 'error',
        title: message || 'Ha ocurrido un error'
    });
}

// Event listeners para HTMX
document.body.addEventListener('htmx:afterSwap', function(event) {
    // Detectar qué acción se realizó basándose en la URL
    const url = event.detail.pathInfo.requestPath;
    
    if (url.includes('/create/') && event.detail.successful) {
        taskCreated();
    } else if (url.includes('/update/') && event.detail.successful) {
        taskUpdated();
    } else if (url.includes('/toggle/') && event.detail.successful) {
        // Detectar si está completada o no desde el HTML retornado
        const content = event.detail.target;
        const isCompleted = content.querySelector('[data-completed="true"]') !== null;
        taskToggled(isCompleted);
    }
});

// Event listener para errores de HTMX
document.body.addEventListener('htmx:responseError', function(event) {
    showError('Error al procesar la solicitud');
});
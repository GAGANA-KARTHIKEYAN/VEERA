/**
 * VEERA — Image validation utilities
 *
 * Validates uploaded images for type, size, and readability.
 */

const ACCEPTED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const ACCEPTED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp'];
const DEFAULT_MAX_SIZE_MB = 10;

/**
 * Returns the configured max file size in bytes.
 */
export function getMaxFileSize() {
  return DEFAULT_MAX_SIZE_MB * 1024 * 1024;
}

/**
 * Formats bytes into a human-readable string.
 */
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB'];
  const k = 1024;
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  const value = bytes / Math.pow(k, i);
  return `${value.toFixed(i > 0 ? 1 : 0)} ${units[i]}`;
}

/**
 * Validates an image file. Returns { valid: true } or { valid: false, error: string }.
 */
export function validateImageFile(file) {
  if (!file) {
    return { valid: false, error: 'No file selected.' };
  }

  // Check MIME type
  if (!ACCEPTED_TYPES.includes(file.type)) {
    const ext = file.name ? file.name.split('.').pop().toLowerCase() : '';
    if (!ACCEPTED_EXTENSIONS.includes(`.${ext}`)) {
      return {
        valid: false,
        error: `Unsupported file type. Please upload a JPEG, PNG, or WebP image.`,
      };
    }
  }

  // Check file size
  const maxSize = getMaxFileSize();
  if (file.size > maxSize) {
    return {
      valid: false,
      error: `File is too large (${formatFileSize(file.size)}). Maximum size is ${DEFAULT_MAX_SIZE_MB} MB.`,
    };
  }

  if (file.size === 0) {
    return {
      valid: false,
      error: 'The file appears to be empty or unreadable.',
    };
  }

  return { valid: true };
}

/**
 * Creates an object URL for local preview. Returns a promise that resolves
 * once the image is confirmed loadable, or rejects if corrupted.
 */
export function createImagePreview(file) {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => {
      resolve({
        url,
        width: img.naturalWidth,
        height: img.naturalHeight,
      });
    };
    img.onerror = () => {
      URL.revokeObjectURL(url);
      reject(new Error('The image file appears to be corrupted or unreadable.'));
    };
    img.src = url;
  });
}

/**
 * Revokes an object URL to free memory.
 */
export function revokeImagePreview(url) {
  if (url && url.startsWith('blob:')) {
    URL.revokeObjectURL(url);
  }
}

import { useCallback, useRef, useState } from 'react';
import { Upload, X, AlertCircle, Image as ImageIcon } from 'lucide-react';
import { formatFileSize } from '../utils/imageValidation.js';

/**
 * VEERA Image Upload Component
 *
 * Supports click-to-select and drag-and-drop.
 * Displays preview with file info when an image is selected.
 * Shows validation errors.
 */
export default function ImageUpload({
  file,
  preview,
  validationError,
  onFileSelect,
  onRemove,
}) {
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  const handleFiles = useCallback(
    (files) => {
      if (files && files.length > 0) {
        onFileSelect(files[0]);
      }
    },
    [onFileSelect]
  );

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    handleFiles(e.dataTransfer.files);
  };

  const handleInputChange = (e) => {
    handleFiles(e.target.files);
    // Reset input so same file can be re-selected
    if (inputRef.current) inputRef.current.value = '';
  };

  const handleReplace = () => {
    inputRef.current?.click();
  };

  // --- Preview state ---
  if (file && preview) {
    return (
      <div className="upload-area">
        <div className="upload-dropzone upload-dropzone--has-file">
          <div className="upload-preview">
            <div className="upload-preview__image-wrap">
              <img
                src={preview.url}
                alt={`Preview of ${file.name}`}
                className="upload-preview__image"
              />
            </div>
            <div className="upload-preview__info">
              <div className="upload-preview__filename">{file.name}</div>
              <div className="upload-preview__meta">
                {formatFileSize(file.size)} · {preview.width}×{preview.height}px
              </div>
              <div className="upload-preview__actions">
                <button
                  className="btn btn--secondary btn--sm"
                  onClick={handleReplace}
                  type="button"
                  aria-label="Replace image"
                >
                  <ImageIcon size={14} aria-hidden="true" />
                  Replace
                </button>
                <button
                  className="btn btn--ghost btn--sm btn--danger"
                  onClick={onRemove}
                  type="button"
                  aria-label="Remove image"
                >
                  <X size={14} aria-hidden="true" />
                  Remove
                </button>
              </div>
            </div>
          </div>
          <input
            ref={inputRef}
            type="file"
            accept="image/jpeg,image/png,image/webp"
            onChange={handleInputChange}
            aria-label="Replace image file"
            style={{ display: 'none' }}
          />
        </div>
        {validationError && (
          <div className="upload-error" role="alert">
            <AlertCircle size={16} className="upload-error__icon" aria-hidden="true" />
            <span>{validationError}</span>
          </div>
        )}
      </div>
    );
  }

  // --- Dropzone state ---
  return (
    <div className="upload-area">
      <div
        className={`upload-dropzone ${dragActive ? 'upload-dropzone--drag-active' : ''}`}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        role="button"
        tabIndex={0}
        aria-label="Upload an image for inspection. Click or drag and drop."
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            inputRef.current?.click();
          }
        }}
      >
        <Upload size={36} className="upload-dropzone__icon" aria-hidden="true" />
        <p className="upload-dropzone__label">
          <strong>Click to upload</strong> or drag and drop
        </p>
        <p className="upload-dropzone__hint">JPEG, PNG, or WebP · Max 10 MB</p>
        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          onChange={handleInputChange}
          aria-label="Select image file"
        />
      </div>
      {validationError && (
        <div className="upload-error" role="alert">
          <AlertCircle size={16} className="upload-error__icon" aria-hidden="true" />
          <span>{validationError}</span>
        </div>
      )}
    </div>
  );
}

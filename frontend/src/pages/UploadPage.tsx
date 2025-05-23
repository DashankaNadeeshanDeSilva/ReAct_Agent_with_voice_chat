import React, { useState, useRef } from 'react';
import { Upload, File, CheckCircle, X, AlertCircle } from 'lucide-react';
import { uploadDocument } from '../utils/api';

interface FileWithPreview extends File {
  preview?: string;
}

const UploadPage: React.FC = () => {
  const [files, setFiles] = useState<FileWithPreview[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragEnter = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    handleFiles(droppedFiles);
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFiles = Array.from(e.target.files);
      handleFiles(selectedFiles);
    }
  };

  const handleFiles = (newFiles: File[]) => {
    const validFiles = newFiles.filter(file => {
      const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
      return validTypes.includes(file.type);
    });

    if (validFiles.length !== newFiles.length) {
      setErrorMessage('Some files were rejected. Only PDF, Word, and text documents are allowed.');
      setTimeout(() => setErrorMessage(''), 5000);
    }

    if (validFiles.length > 0) {
      setFiles(prevFiles => [...prevFiles, ...validFiles]);
    }
  };

  const removeFile = (indexToRemove: number) => {
    setFiles(prevFiles => prevFiles.filter((_, index) => index !== indexToRemove));
  };

  const handleUpload = async () => {
    if (files.length === 0) return;

    setUploadStatus('uploading');
    setErrorMessage('');

    try {
      for (const file of files) {
        const response = await uploadDocument(file);
        
        if (response.error) {
          throw new Error(response.error);
        }
      }

      setUploadStatus('success');
      
      // Reset after showing success
      setTimeout(() => {
        setFiles([]);
        setUploadStatus('idle');
      }, 3000);
    } catch (error) {
      setUploadStatus('error');
      setErrorMessage(error instanceof Error ? error.message : 'Upload failed');
      
      setTimeout(() => {
        setUploadStatus('idle');
        setErrorMessage('');
      }, 5000);
    }
  };

  const triggerFileInput = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const getFileIcon = (fileType: string) => {
    if (fileType.includes('pdf')) {
      return <File className="h-8 w-8 text-red-500" />;
    } else if (fileType.includes('word') || fileType.includes('document')) {
      return <File className="h-8 w-8 text-blue-500" />;
    } else {
      return <File className="h-8 w-8 text-gray-500" />;
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold text-gray-900 mb-3">Upload Your Documents</h1>
        <p className="text-gray-600">
          Upload your documents to index them to the vector database for retrieval during chat.
        </p>
      </div>

      {errorMessage && (
        <div className="mb-6 p-3 bg-red-50 border border-red-200 rounded-md flex items-center text-red-700">
          <AlertCircle className="h-5 w-5 mr-2 flex-shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      <div 
        className={`border-2 border-dashed rounded-lg p-8 transition-colors duration-200 text-center ${
          isDragging 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-blue-400'
        }`}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileInputChange}
          className="hidden"
          multiple
          accept=".pdf,.doc,.docx,.txt"
        />

        <div className="flex flex-col items-center justify-center space-y-4">
          <div className="bg-blue-100 rounded-full p-3">
            <Upload className="h-8 w-8 text-blue-600" />
          </div>
          <h3 className="text-lg font-medium text-gray-900">
            {isDragging ? 'Drop your files here' : 'Drag & Drop your files here'}
          </h3>
          <p className="text-sm text-gray-500">
            or
          </p>
          <button
            type="button"
            onClick={triggerFileInput}
            className="px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Browse Files
          </button>
          <p className="text-xs text-gray-500 mt-2">
            Supported formats: PDF, Word, TXT
          </p>
        </div>
      </div>

      {files.length > 0 && (
        <div className="mt-8">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Selected Files</h3>
          <div className="space-y-3">
            {files.map((file, index) => (
              <div 
                key={`${file.name}-${index}`}
                className="flex items-center justify-between p-3 bg-white border border-gray-200 rounded-md hover:shadow-sm transition-shadow duration-200"
              >
                <div className="flex items-center space-x-3">
                  {getFileIcon(file.type)}
                  <div>
                    <p className="text-sm font-medium text-gray-900 truncate max-w-xs">{file.name}</p>
                    <p className="text-xs text-gray-500">{(file.size / 1024).toFixed(2)} KB</p>
                  </div>
                </div>
                <button 
                  type="button"
                  onClick={() => removeFile(index)}
                  className="p-1 text-gray-400 hover:text-red-500 transition-colors duration-200"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            ))}
          </div>

          <div className="mt-6">
            <button
              type="button"
              onClick={handleUpload}
              disabled={uploadStatus === 'uploading'}
              className={`w-full flex items-center justify-center px-4 py-3 rounded-md text-white font-medium ${
                uploadStatus === 'uploading' 
                  ? 'bg-blue-400 cursor-not-allowed' 
                  : uploadStatus === 'success'
                    ? 'bg-green-500 hover:bg-green-600'
                    : 'bg-blue-600 hover:bg-blue-700'
              } transition-colors duration-200 shadow-sm`}
            >
              {uploadStatus === 'uploading' && (
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              )}
              {uploadStatus === 'success' && <CheckCircle className="mr-2 h-5 w-5" />}
              {uploadStatus === 'uploading' ? 'Uploading...' : uploadStatus === 'success' ? 'Uploaded Successfully!' : 'Upload Files'}
            </button>
          </div>
        </div>
      )}

      <div className="mt-12 p-6 bg-gray-50 rounded-lg border border-gray-200">
        <h3 className="text-lg font-medium text-gray-900 mb-2">What happens next?</h3>
        <p className="text-gray-600 text-sm mb-4">
          After uploading, your documents will be processed and indexed to our vector database.
          This process extracts meaningful information that can be quickly retrieved when you ask questions.
        </p>
        <p className="text-gray-600 text-sm">
          Once processing is complete, you can start chatting with your documents in the Chat section.
        </p>
      </div>
    </div>
  );
};

export default UploadPage;
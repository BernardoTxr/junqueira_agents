// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck

import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

interface InputzoneProps {
  setCarregando: React.Dispatch<React.SetStateAction<boolean>>;
  apiURL?: string;
  setResultadosAnalise?: React.Dispatch<React.SetStateAction<{ [key: string]: string }>>;
  setResultadoCarregado?: React.Dispatch<React.SetStateAction<boolean>>;
}

export function Inputzone({ setCarregando, apiURL, setResultadosAnalise, setResultadoCarregado }: InputzoneProps) {
  const [acceptedFiles, setAcceptedFiles] = React.useState<File[]>([]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setAcceptedFiles((prevFiles) => [...prevFiles, ...acceptedFiles]);
  }, []);

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  function enviarArquivos() {
    setCarregando(true);

    const apiUrl = "http://104.154.164.226:8000/processar";
    const formData = new FormData();

    acceptedFiles.forEach((file) => {
      formData.append('files', file);
    });

    fetch(apiUrl, {
      method: 'POST',
      body: formData,
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Erro ao enviar arquivos');
        }
        return response.json();
      })
      .then(data => {
        const payload = {
          message: data.message,
          filenames: data.filenames,
        };

        console.log('Sucesso:', data.message);

        return fetch("http://104.154.164.226:8001/processar", {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Erro ao processar os arquivos');
        }
        return response.json();
      })
      .then(processedData => {
            console.log('Processed data completo:', processedData);

            // Aqui, você já salva o objeto completo com todos os relatórios
            setResultadosAnalise?.(processedData); // processedData já está no formato { "filename.pdf": "base64" }

            setCarregando(false);
            setResultadoCarregado?.(true);
        })


      .catch(error => {
        console.error('Erro:', error);
        setCarregando(false);
      });
  }

  function removerArquivo(index: number) {
    setAcceptedFiles(prevFiles => prevFiles.filter((_, i) => i !== index));
  }

  function formatFileSize(bytes: number) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  return (
    <div className='flex flex-col flex-1/4'>
      <div className='bg-blue-50 border-blue-200 border-2 border-b-0 rounded-t-lg mb-0 flex flex-col flex-1 justify-center items-center' {...getRootProps()}>
        <input {...getInputProps()} />
        <div className='flex flex-2/3 items-center justify-center flex-col'>
          <p className='mb-2 w-8/10 cursor-pointer text-gray-500 text-2xl text-center rounded-lg relative '>
            Selecione ou Coloque os arquivos aqui
          </p>
        </div>

        {/* Lista de Arquivos */}
        {acceptedFiles.length > 0 && (
          <div className='flex-1/3 flex justify-center items-center w-full'>
            <div className='bg-gray-50 border-2 border-blue-200 rounded-lg max-h-100 h-100 mb-0 overflow-y-auto w-9/10'>
              <div className='p-3'>
                <h4 className='text-sm font-medium text-gray-700 mb-2 text-center'>
                  Arquivos selecionados ({acceptedFiles.length}):
                </h4>
                <div className='space-y-2'>
                  {acceptedFiles.map((file, index) => (
                    <div key={index} className='flex items-center justify-between bg-white p-2 rounded border'>
                      <div className='flex-1 min-w-0'>
                        <p className='text-sm font-medium text-gray-900 truncate'>
                          {file.name}
                        </p>
                        <p className='text-xs text-gray-500'>
                          {formatFileSize(file.size)}
                        </p>
                      </div>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          removerArquivo(index);
                        }}
                        className='ml-2 text-red-500 hover:text-red-700 text-sm font-medium'
                      >
                        Remover
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className='bg-blue-50 border-blue-200 border-2 h-fit pt-2 pb-8 border-t-0 rounded-b-lg flex justify-center items-center'>
        <button
          className='z-10 bg-blue-950 text-white mt-0 p-3 rounded-lg cursor-pointer w-9/10 hover:bg-blue-900 transition-colors disabled:opacity-50 disabled:cursor-not-allowed'
          onClick={enviarArquivos}
          disabled={acceptedFiles.length === 0}
        >
          Enviar Arquivos {acceptedFiles.length > 0 && `(${acceptedFiles.length})`}
        </button>
      </div>
    </div>
  );
}

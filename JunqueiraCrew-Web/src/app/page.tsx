// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck

'use client';
import React, { useState } from 'react';
import { FileText, Download, Upload } from 'lucide-react';
import { Inputzone } from './components/Inputzone';
import { ClipLoader } from "react-spinners";

export default function ReportViewer() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [carregando, setCarregando] = useState(false);
  const [resultado_carregado, setResultadoCarregado] = useState(false);
  const [resultados_analise, setResultadosAnalise] = useState<{ [key: string]: string }>({});

  const handleDownload = () => {
  if (!resultado_carregado || !resultados_analise || Object.keys(resultados_analise).length === 0) {
    alert('Nenhum relatório disponível para download.');
    return;
  }

  Object.entries(resultados_analise).forEach(([fileName, base64]) => {
  // Detecta o tipo de arquivo pela extensão
  let mimeType = 'application/octet-stream'; // padrão seguro

  if (fileName.toLowerCase().endsWith('.pdf')) {
    mimeType = 'application/pdf';
  } else if (fileName.toLowerCase().endsWith('.csv')) {
    mimeType = 'text/csv';
  }

  const blob = base64ToBlob(base64, mimeType);
  const url = URL.createObjectURL(blob);

  const link = document.createElement('a');
  link.href = url;
  link.download = fileName; // Usa o nome original
  document.body.appendChild(link);
  link.click();

  document.body.removeChild(link);
  URL.revokeObjectURL(url);
});

};


  function base64ToBlob(base64: string, mimeType: string) {
    const byteCharacters = atob(base64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mimeType });
  }



  

  return (
    <div className="min-h-screen h-screen flex flex-col bg-white">
      {/* Barra Superior */}
      <header className="bg-blue-900 text-white p-4 h-fit shadow-md">
        <h1 className="text-2xl font-semibold text-center">
          Analista FIDCs
        </h1>
      </header>
      {/* Conteudo Principal */}
      <div className="w-screen h-8/10  flex-1 scroll-hidden mx-auto p-6 pl-20 pr-20  gap-10 space-y-8 flex flex-row">
        {/* Área de Input */}
        <Inputzone setCarregando={setCarregando} setResultadosAnalise={ setResultadosAnalise } setResultadoCarregado={setResultadoCarregado}/>
        {/* Área de Resultados */}
        <div className="bg-gray-50 flex-3/4 border-2 border-gray-200 rounded-lg h-192 flex flex-col items-center justify-center">
          {/*Report*/}
          <div className="text-center text-gray-500 flex-3/4 w-10/10 items-center justify-center flex">
          {carregando ? (
              <>
                <div className='flex flex-col items-center justify-center mb-4'>
                  <ClipLoader color="#0000FF" size={50} className="mx-auto mb-4" loading={true} />
                  <p className='text-gray-400'>Processando Requisição</p>
                </div>
              </>    
            ) : 
            (
              !resultado_carregado ? (
                <div>
                  <FileText size={48} className="mx-auto mb-4 text-gray-400 " />
                  <p className="text-lg">Aguardando Relatório</p>
                </div>
              ) : (
                  <div>
                  <FileText size={48} className="mx-auto mb-4 text-gray-400 " />
                  <p className="text-lg">Relatório pronto para Download!</p>
                </div>
              )
            )
          }
          </div>
          {/* Botão de Download */}
          <div className="text-center p-6">
            <button
              onClick={handleDownload}
              disabled={!resultado_carregado}
              className={`inline-flex items-center px-6 py-3 rounded-lg font-medium transition-colors  ${
                resultado_carregado
                  ? 'bg-blue-900 text-white hover:bg-blue-800 cursor-pointer'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              <Download size={20} className="mr-2" />
              Baixar Relatório
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
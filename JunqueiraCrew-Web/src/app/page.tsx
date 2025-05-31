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
    // Simula download do relatório
    alert('Download do relatório iniciado!');
  };

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
                  <iframe
                    src={`data:application/pdf;base64,${resultados_analise.relatorio_final}`}
                    title="Relatório FIDC"
                    className="w-full h-full"
                    allow="fullscreen"
                  />
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
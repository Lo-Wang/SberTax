'use client';

import { useState } from 'react';
import TransactionList from '@/app/components/transactionList';
import DownloadTemplateButton from '@/app/components/downloadTemplateButton';
import UploadFileButton from '@/app/components/uploadFileButton';
import ContinueButton from '@/app/components/continueButton';
import { useRouter } from 'next/navigation';
import './styles.css';

export default function ApplicationSubmission() {
    const router = useRouter();
    const [selectedFile, setSelectedFile] = useState(null);
    const [fileName, setFileName] = useState('');
    const [selectedTransaction, setSelectedTransaction] = useState(null);

    const handleFileUpload = (file) => {
        setSelectedFile(file);
        setFileName(file.name);
    };

    const handleBackClick = () => {
        router.push('/pages/dashboard');
    };

    const handleTransactionSelect = (transaction) => {
        console.log('Выбрана транзакция:', transaction);
        setSelectedTransaction(transaction);
    };

    return (
        <div className="container">
            <h1 className="title">Выберите транзакцию</h1>
            <TransactionList onSelectTransaction={handleTransactionSelect} />
            <div className="button-container">
                <DownloadTemplateButton />
                <UploadFileButton onFileUpload={handleFileUpload} />
                <ContinueButton
                    selectedTransaction={selectedTransaction}
                    fileName={fileName}
                />
                <button className="button_back" onClick={handleBackClick}>
                    <strong>Назад</strong>
                </button>
            </div>
        </div>
    );
}

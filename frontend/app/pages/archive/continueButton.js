'use client';

import { useRouter } from 'next/navigation';

export default function ContinueButton({ selectedTransaction, fileName }) {
    const router = useRouter();

    const handleSubmit = async () => {
        if (!selectedTransaction) {
            alert('Пожалуйста, выберите транзакцию.');
            return;
        }

        if (!fileName) {
            alert('Пожалуйста, загрузите файл.');
            return;
        }

        const applicationData = {
            id: new Date().getTime(),
            transactionId: selectedTransaction.id,
            submissionDate: new Date().toISOString(),
            category: selectedTransaction.category,
            amount: selectedTransaction.amount,
            status: 'Отправлено',
            transactionDate: selectedTransaction.date,
            mccCode: selectedTransaction.mcc_code,
            description: selectedTransaction.description,
            fileName: fileName,
        };

        try {
            const response = await fetch('/api/saveApplication', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(applicationData),
            });

            if (!response.ok) {
                throw new Error('Ошибка при отправке заявки');
            }

            const data = await response.json();
            console.log(data.message);
            router.push('/pages/submission-confirmation');
        } catch (error) {
            console.error('Ошибка:', error);
        }
    };

    return (
        <button className="button" onClick={handleSubmit}>
            Продолжить
        </button>
    );
}

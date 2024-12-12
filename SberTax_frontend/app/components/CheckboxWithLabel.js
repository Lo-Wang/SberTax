'use client';

import { useState } from 'react';
import styles from './CheckboxWithLabel.module.css';

export default function CheckboxWithLabel() {
  const [isChecked, setIsChecked] = useState(false);

  const handleCheckboxChange = (event) => {
    setIsChecked(event.target.checked);
    console.log('Состояние чекбокса:', event.target.checked);
  };

  return (
    <div className={styles.checkboxContainer}>
      <input
        type="checkbox"
        id="agreementCheckbox"
        checked={isChecked}
        onChange={handleCheckboxChange}
        className={styles.checkbox}
      />
      <label htmlFor="agreementCheckbox" className={styles.label}>
        Соглашение на обработку данных
      </label>
    </div>
  );
}

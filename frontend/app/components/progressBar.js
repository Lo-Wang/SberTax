'use client';

import './progressBar.css';

export default function ProgressBar({ coins, maxCoins }) {
  const progressPercentage = (coins / maxCoins) * 100;

  return (
    <div className="progress-container">
      <div className="progress-header">
        <span>Заработано:</span>
        <span>{`${coins} руб.`}</span>
      </div>
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{
            width: `${progressPercentage}%`,
            background: 'linear-gradient(90deg, #66ff00 0%, #21A038 130%)',
          }}
        ></div>
      </div>
      <div className="progress-footer">
        <span>Детальней</span>
        <span className="max-coins">{`${maxCoins} руб.`}</span>
      </div>
    </div>
  );
}

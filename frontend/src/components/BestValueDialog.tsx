import { BestValueResult } from '../types';

/**
 * BestValueDialog — BONUS CHALLENGE #2
 *
 * Displays the results from the Best Value Finder API.
 */

interface BestValueDialogProps {
  result: BestValueResult;
  budget: number;
  onClose: () => void;
  onApply: () => void;
}
// Format: "15 Jun, 19:00" - British format for consistency
function BestValueDialog({ result, budget, onClose, onApply }: BestValueDialogProps) {
  const { withinBudget, matches, costBreakdown, countriesVisited, matchCount, message } = result;

  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog-content" onClick={(e) => e.stopPropagation()}>
        <div className="dialog-header">
          <h2>Best Value Matches</h2>
          <button className="dialog-close" onClick={onClose}>&times;</button>
        </div>

        <div className="dialog-body">
          {/* Status Message */}
          <div className={`best-value-status ${withinBudget ? 'within-budget' : 'over-budget'}`}>
            <span className="status-icon">{withinBudget ? '\u2713' : '\u26A0'}</span>
            <span>{message}</span>
          </div>

          {/* Cost Summary - FIXED FIELD NAMES */}
          {costBreakdown && (
            <div className="best-value-costs">
              <h4>Cost Breakdown</h4>
              <div className="cost-row">
                <span>Flights</span>
                <span>${costBreakdown.flightCost.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
              </div>
              <div className="cost-row">
                <span>Accommodation</span>
                <span>${costBreakdown.accommodationCost.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
              </div>
              <div className="cost-row">
                <span>Match Tickets</span>
                <span>${costBreakdown.ticketCost.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
              </div>
              <div className={`cost-row cost-total ${!withinBudget ? 'over-budget' : ''}`}>
                <span>Total</span>
                <span>${costBreakdown.totalCost.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
              </div>
              <div className="cost-row budget-row">
                <span>Your Budget</span>
                <span>${budget.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
              </div>
            </div>
          )}

          {/* Countries */}
          <div className="best-value-countries">
            <h4>Countries Visited ({countriesVisited.length}/3)</h4>
            <div className="country-tags">
              {countriesVisited.map((country) => (
                <span key={country} className="country-tag">{country}</span>
              ))}
            </div>
          </div>

          {/* Matches List */}
          <div className="best-value-matches">
            <h4>Recommended Matches ({matchCount})</h4>
            <ul className="match-list">
              {matches.map((match) => {
                // Handle both string and object formats for teams/cities (API can return either)
                const homeTeam = typeof match.homeTeam === 'string' ? match.homeTeam : match.homeTeam?.name;
                const awayTeam = typeof match.awayTeam === 'string' ? match.awayTeam : match.awayTeam?.name;
                const cityName = typeof match.city === 'string' ? match.city : match.city?.name;
                const kickoff = new Date(match.kickoff);
                const dateStr = kickoff.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
                const timeStr = kickoff.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
                return (
                  <li key={match.id} className="match-item">
                    <div className="match-teams">
                      {homeTeam} vs {awayTeam}
                    </div>
                    <div className="match-details">
                      <span>{cityName}</span>
                      <span>{dateStr}, {timeStr}</span>
                      <span className="ticket-price">${match.ticketPrice}</span>
                    </div>
                  </li>
                );
              })}
            </ul>
          </div>
        </div>

        <div className="dialog-footer">
          <button className="btn btn-secondary" onClick={onClose}>
            Cancel
          </button>
          <button className="btn btn-primary" onClick={onApply}>
            Apply Selection
          </button>
        </div>
      </div>
    </div>
  );
}

export default BestValueDialog;
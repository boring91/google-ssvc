export const assessmentStyles: Record<string, Record<string, string>> = {
    action: {
        track: 'bg-green-500/20 text-green-300',
        // eslint-disable-next-line @typescript-eslint/naming-convention
        'track*': 'bg-yellow-500/20 text-yellow-300',
        attend: 'bg-orange-500/20 text-orange-300',
        act: 'bg-red-500/20 text-red-300',
    },
    automatability: {
        yes: 'bg-red-500/20 text-red-300',
        no: 'bg-green-500/20 text-green-300',
    },
    exploitation: {
        none: 'bg-green-500/20 text-green-300',
        poc: 'bg-yellow-500/20 text-yellow-300',
        active: 'bg-red-500/20 text-red-300',
    },
    exposure: {
        small: 'bg-green-500/20 text-green-300',
        controlled: 'bg-yellow-500/20 text-yellow-300',
        open: 'bg-red-500/20 text-red-300',
    },
    missionImpact: {
        degraded: 'bg-yellow-500/20 text-yellow-300',
        // eslint-disable-next-line @typescript-eslint/naming-convention
        mef_support_crippled: 'bg-orange-500/20 text-orange-300',
        // eslint-disable-next-line @typescript-eslint/naming-convention
        mef_failure: 'bg-red-500/20 text-red-300',
        // eslint-disable-next-line @typescript-eslint/naming-convention
        mission_failure: 'bg-red-700/20 text-red-400',
    },
    missionPrevalence: {
        minimal: 'bg-green-500/20 text-green-300',
        support: 'bg-yellow-500/20 text-yellow-300',
        essential: 'bg-red-500/20 text-red-300',
    },
    publicWellbeing: {
        minimal: 'bg-green-500/20 text-green-300',
        material: 'bg-yellow-500/20 text-yellow-300',
        irreversible: 'bg-red-500/20 text-red-300',
    },
    technicalImpact: {
        partial: 'bg-yellow-500/20 text-yellow-300',
        total: 'bg-red-500/20 text-red-300',
    },
    valueDensity: {
        centralized: 'bg-yellow-500/20 text-yellow-300',
        diffused: 'bg-green-500/20 text-green-300',
    },
} as const;

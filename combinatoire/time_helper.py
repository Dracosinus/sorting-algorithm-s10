def divide_mins_to_days_hours_mins(duree_minutes):
    jours = duree_minutes // (24 * 60)
    heures = (duree_minutes // 60) % 24
    minutes = duree_minutes % 60
    return (jours, heures, minutes)

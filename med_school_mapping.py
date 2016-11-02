import numpy as np


MEDSCHOOL_MAPPING = [
    ('SOUTH ALABAMA', 'UNIVERSITY OF SOUTH ALABAMA COLLEGE OF MEDICINE'),
    ('UNIVERSITY OF ALA', 'UNIVERSITY OF ALABAMA SCHOOL OF MEDICINE'),
    ('ALABAMA', 'UNIVERSITY OF ALABAMA SCHOOL OF MEDICINE'),
    ('MEDICAL COLLEGE OF ALABAMA', 'UNIVERSITY OF ALABAMA SCHOOL OF MEDICINE'),
    ('ARKANSAS', 'UNIVERSITY OF ARKANSAS SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF ARK', 'UNIVERSITY OF ARKANSAS SCHOOL OF MEDICINE'),
    ('ALBANY', 'ALBANY MEDICAL COLLEGE'),
    ('BAYLOR', 'BAYLOR COLLEGE OF MEDICINE'),
    ('BOSTON UNIVERSITY', 'BOSTON UNIVERSITY SCHOOL OF MEDICINE'),
    ('BROWN', 'BROWN MEDICAL SCHOOL'),
    ('BUFFALO', 'SUNY BUFFALO SCHOOL OF MEDICINE & BIOMEDICAL SCIENCES'),
    ('CASE WESTERN', 'CASE WESTERN RESERVE UNIVERSITY SCHOOL OF MEDICINE'),
    ('WESTERN RESERVE', 'CASE WESTERN RESERVE UNIVEESITY SCHOOL OF MEDICINE'),
    ('CWRU', 'CASE WESTERN RESERVE UNIVEESITY SCHOOL OF MEDICINE'),
    ('FINCH', 'FINCH UNIVERSITY OF HEALTH SCIENCES'),
    ('CHICAGO MEDICAL', 'THE CHICAGO MEDICAL SCHOOL'),
    ('PRITZKER', 'UNIVERSITY OF CHICAGO'), ('UNIVERSITY OF CHICAGO', 'UNIVERSITY OF CHICAGO'),
    ('CINCINNATI', 'UNIVERSITY OF CINCINNATI COLLEGE OF MEDICINE'),

    ('COLORADO HEALTH', 'UNIVERSITY OF COLORADO HEALTH SCIENCES CENTER SCHOOL OF MEDICINE - DENVER'),
    (' DENVER', 'UNIVERSITY OF COLORADO HEALTH SCIENCES CENTER SCHOOL OF MEDICINE - DENVER'),
    ('COLORADO', 'UNIVERSITY OF COLORADO HEALTH SCIENCES CENTER SCHOOL OF MEDICINE - DENVER'),
    ('UNIVERSITY OF COLORADO MEDICAL', 'UNIVERSITY OF COLORADO HEALTH SCIENCES CENTER SCHOOL OF MEDICINE - DENVER'),
    ('UNIVERSITY OF COLO', 'UNIVERSITY OF COLORADO HEALTH SCIENCES CENTER SCHOOL OF MEDICINE - DENVER'),

    ('COLUMBIA', 'COLUMBIA UNIVERSITY COLLEGE OF PHYSICIANS AND SURGEONS'),
    ('PHYSICIANS', 'COLUMBIA UNIVERSITY COLLEGE OF PHYSICIANS AND SURGEONS'),
    ('P S', 'COLUMBIA UNIVERSITY COLLEGE OF PHYSICIANS AND SURGEONS'),
    ('COLLEGE OF P S', 'COLUMBIA UNIVERSITY COLLEGE OF PHYSICIANS AND SURGEONS'),
    ('WEILL', 'JOAN & SANFORD I. WEILL MEDICAL COLLEGE CORNELL UNIVERSITY'),
    ('CORNELL', 'JOAN & SANFORD I. WEILL MEDICAL COLLEGE CORNELL UNIVERSITY'),
    ('CREIGHTON', 'CREIGHTON UNIVERSITY SCHOOL OF MEDICINE'),
    ('DREW', 'CHARLES R DREW UNIVERSITY SCHOOL OF MEDICINE'),
    ('EAST TENNESSEE', 'EAST TENNESSEE STATE UNIVERSITY JAMES H. QUILLEN COLLEGE OF MEDICINE'),
    ('EASTERN VIRGINAIA', 'EASTERN VIRGINIA MEDICAL SCHOOL'),
    ('FLORIDA', 'UNIVERSITY OF FLORIDA COLLEGE OF MEDICINE'),
    ('DARTMOUTH', 'DARTMOUTH MEDICAL SCHOOL'),
    ('DUKE', 'DUKE MEDICAL SCHOOL'),
    ('ALBERT EINSTEIN', 'ALBERT EINSTEIN COLLEGE OF MEDICINE OF YESHIVA UNIVERSITY'),
    ('YESHIVA', 'ALBERT EINSTEIN COLLEGE OF MEDICINE OF YESHIVA UNIVERSITY'),
    ('ALBERT', 'ALBERT EINSTEIN COLLEGE OF MEDICINE OF YESHIVA UNIVERSITY'),
    ('EINSTEIN', 'ALBERT EINSTEIN COLLEGE OF MEDICINE OF YESHIVA UNIVERSITY'),
    ('EMORY', 'EMORY UNIVERSITY SCHOOL OF MEDICINE'),
    ('GEORGETOWN', 'GEORGETOWN UNIVERSITY SCHOOL OF MEDICINE'),
    ('GEORGETWON', 'GEORGETOWN UNIVERSITY SCHOOL OF MEDICINE'),
    ('GEORGE WASHINGTON', 'GEORGE WASHINGTON UNIVERSITY SCHOOL OF MEDICINE'),
    ('G W U', 'GEORGE WASHINGTON UNIVERSITY SCHOOL OF MEDICINE'),
    ('GEORGIA', 'MEDICAL COLLEGE OF GEORGIA SCHOOL OF MEDICINE'),
    ('MEDICAL COLLEGE OF OHIO', 'MEDICAL COLLEGE OF OHIO'),
    ('MEDICAL COLLEGE OF WISCONSIN', 'MEDICAL COLLEGE OF WISCONSIN'),
    ('MIT', 'MIT'),
    ('HAHNEMANN ', 'HAHNEMANN SCHOOL OF MEDICINE'),
    ('HANNEMANN', 'HAHNEMANN SCHOOL OF MEDICINE'),
    ('HAHREMANN', 'HAHNEMANN SCHOOL OF MEDICINE'),
    ('HAUNEMANN', 'HAHNEMANN SCHOOL OF MEDICINE'),
    ('HARVARD', 'HARVARD MEDICAL SCHOOL'),
    ('HOWARD', 'HOWARD UNIVERSITY COLLEGE OF MEDICINE'),
    ('ILLINOIS', 'UNIVERSITY OF ILLINOIS COLLEGE OF MEDICINE'),
    ('OF ILL', 'UNIVERSITY OF ILLINOIS COLLEGE OF MEDICINE'),
    ('INDIANA', 'INDIANA UNIVERSITY SCHOOL OF MEDICINE'),
    ('INDIAN UNIVERSITY', 'INDIANA UNIVERSITY SCHOOL OF MEDICINE'),
    ('IRVINE', 'UC IRVINE COLLEGE OF MEDICINE'),
    ('IOWA', 'UNIVERSITY OF IOWA COLLEGE OF MEDICINE'),
    ('JEFFERSON', 'JEFFERSON MEDICAL COLLEGE OF THOMAS JEFFERSON UNIVERSITY'),
    (' THOMAS', 'JEFFERSON MEDICAL COLLEGE OF THOMAS JEFFERSON UNIVERSITY'),
    ('HOPKINS', 'JOHNS HOPKINS UNIVERSITY SCHOOL OF MEDICINE'),
    ('KANSAS', 'UNIVERSITY OF KANSAS SCHOOL OF MEDICINE'),
    ('KENTUCKY', 'UNIVERSITY OF KENTUCKY COLLEGE OF MEDICINE'),
    ('DOWNSTATE', 'SUNY DOWNSTATE MEDICAL CENTER COLLEGE OF MEDICINE'),
    ('BROOKLYN', 'SUNY DOWNSTATE MEDICAL CENTER COLLEGE OF MEDICINE'),
    ('EAST CAROLINA', 'THE BRODY SCHOOL OF MEDICINE AT EAST CAROLINA UNIVERSITY'),
    ('NEW ORLEANS', 'LOUISIANA STATE UNIVERSITY SCHOOL OF MEDICINE IN NEW ORLEANS'),
    ('LSU', 'LOUISIANA STATE UNIVERSITY SCHOOL OF MEDICINE IN NEW ORLEANS'),
    ('SHREVEPORT', 'LOUISIANA STATE UNIVERSITY SCHOOL OF MEDICINE IN SHREVEPORT'),
    # CATCHALL FOR
    ('LOUISIANA', 'LOUISIANA STATE UNIVERSITY SCHOOL OF MEDICINE IN NEW ORLEANS'),
    ('LOUISVILLE', 'UNIVERSITY OF LOUISVILLE SCHOOL OF MEDICINE'),
    ('LOYOLA', 'LOYOLA UNIVERSITY CHICAGO STRITCH SCHOOL OF MEDICINE'),
    ('MARSHALL', 'MARSHALL UNIVERSITY'),
    ('MIAMI', 'UNIVERSITY OF MIAMI SCHOOL OF MEDICINE'),
    ('LEONARD MILLER', 'UNIVERSITY OF MIAMI SCHOOL OF MEDICINE'),
    ('WISCONSIN', 'MEDICAL COLLEGE OF WISCONSIN'),
    ('MARYLAND', 'UNIVERSITY OF MARYLAND SCHOOL OF MEDICINE'),
    ('LOMA LINDA', 'LOMA LINDA UNIVERSITY SCHOOL OF MEDICINE'),
    ('MEHARRY', 'MEHARRY MEDICAL COLLEGE'),
    ('MELARRY', 'MEHARRY MEDICAL COLLEGE'),
    ('MERCER', 'MERCER UNIVERSITY SCHOOL OF MEDICINE'),
    ('MICHIGAN STATE', 'MICHIGAN STATE UNIVERSITY COLLEGE OF HUMAN MEDICINE'),
    ('UNIVERSITY OF MICH', 'UNIVERSITY OF MICHIGAN MEDICAL SCHOOL'),
    ('MOUNT SINAI', 'MOUNT SINAI SCHOOL OF MEDICINE OF NEW YORK UNIVERSITY'),
    ('MT SINAI', 'MOUNT SINAI SCHOOL OF MEDICINE OF NEW YORK UNIVERSITY'),
    ('ICAHN ', 'MOUNT SINAI SCHOOL OF MEDICINE OF NEW YORK UNIVERSITY'),

    ('OF MASSACHUSETTS', 'UNIVERSITY OF MASSACHUSETTS'),
    ('OF MA', 'UNIVERSITY OF MASSACHUSETTS'),
    (' MA ', 'UNIVERSITY OF MASSACHUSETTS'),
    ('MICHIGAN', 'UNIVERSITY OF MICHIGAN MEDICAL SCHOOL'),
    ('TWIN CITIES', 'UNIVERSITY OF MINNESOTA MEDICAL SCHOOL - TWIN CITIES'),
    ('DULUTH', 'UNIVERSITY OF MINNESOTA MEDICAL SCHOOL - DULUTH'),
    ('MINNESOTA', 'UNIVERSITY OF MINNESOTA MEDICAL SCHOOL'),
    ('UNIVERSITY OF MINN', 'UNIVERSITY OF MINNESOTA MEDICAL SCHOOL'),
    ('MISSISSIPPI', 'UNIVERSITY OF MISSISSIPPI SCHOOL OF MEDICINE'),
    ('MISSOURI', 'UNIVERSITY OF MISSOURI-COLUMBIA SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF MO', 'UNIVERSITY OF MISSOURI-COLUMBIA SCHOOL OF MEDICINE'),
    ('NEBRASKA', 'UNIVERSITY OF NEBRASKA COLLEGE OF MEDICINE'),
    ('NEW MEXICO', 'UNIVERSITY OF NEW MEXICO SCHOOL OF MEDICINE'),
    ('NEW YORK MEDICAL', 'NEW YORK MEDICAL COLLEGE'),
    ('NEW YORK UNIVERSITY', 'NEW YORK UNIVERSITY COLLEGE OF MEDICINE'),
    ('STATE UNIVERSITY OF NEW YORK', 'NEW YORK UNIVERSITY COLLEGE OF MEDICINE'),
    ('N Y U', 'NYU'),
    ('NYU', 'NEW YORK UNIVERSITY COLLEGE OF MEDICINE'),
    ('NEW YORK', 'NEW YORK UNIVERSITY COLLEGE OF MEDICINE'),
    ('NORTH CAROLINA', 'UNIVERSITY OF NORTH CAROLINA AT CHAPEL HILL SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF N C', 'UNIVERSITY OF NORTH CAROLINA AT CHAPEL HILL SCHOOL OF MEDICINE'),
    ('CHAPEL HILL', 'UNIVERSITY OF NORTH CAROLINA AT CHAPEL HILL SCHOOL OF MEDICINE'),
    ('NORTH DAKOTA', 'UNIVERSITY OF NORTH DAKOTA SCHOOL OF MEDICINE AND HEALTH SCIENCES'),
    ('NORTHWESTERN', 'NORTHWESTERN UNIVERSITY MEDICAL SCHOOL'),
    ('NORTH WESTERN', 'NORTHWESTERN UNIVERSITY MEDICAL SCHOOL'),
    ('OHIO STATE', 'OHIO STATE UNIVERSITY COLLEGE OF MEDICINE AND PUBLIC HEALTH'),
    ('OKLAHOMA', 'UNIVERSITY OF OKLAHOMA COLLEGE OF MEDICINE'),
    ('UNIVERSITY OF OK', 'UNIVERSITY OF OKLAHOMA COLLEGE OF MEDICINE'),
    ('OREGON HEALTH ', 'OREGON HEALTH SCIENCES UNIVERSITY SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF OREGON', 'OREGON HEALTH SCIENCES UNIVERSITY SCHOOL OF MEDICINE'),

    ('PENNSYLVANIA STATE', 'PENNSYLVANIA STATE UNIVERSITY COLLEGE OF MEDICINE'),
    ('HERSHEY', 'PENNSYLVANIA STATE UNIVERSITY COLLEGE OF MEDICINE'),
    ('PENN STATE', 'PENNSYLVANIA STATE UNIVERSITY COLLEGE OF MEDICINE'),
    ('PERELMAN SCHOOL', 'UNIVERSITY OF PENNSYLVANIA SCHOOL OF MEDICINE'),
    ('PENNSYLVANIA', 'UNIVERSITY OF PENNSYLVANIA SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF PA', 'UNIVERSITY OF PENNSYLVANIA SCHOOL OF MEDICINE'),
    ('PENNSLYVANIA', 'UNIVERSITY OF PENNSYLVANIA SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF PENN', 'UNIVERSITY OF PENNSYLVANIA SCHOOL OF MEDICINE'),
    ('SAN ANTONIO', 'UNIVERSITY OF TEXAS MEDICAL SCHOOL AT SAN ANTONIO'),
    ('HOUSTON', 'UNIVERSITY OF TEXAS HEALTH SCIENCES CENTER AT HOUSTON'),
    ('UNIVERSITY OF TEXAS', 'UNIVERSITY OF TEXAS HEALTH SCIENCES CENTER AT HOUSTON'),

    ('PUERTO RICO', 'UNIVERSITY OF PUERTO RICO SCHOOL OF MEDICINE'),
    ('PITTSBURGH', 'UNIVERSITY OF PITTSBURGH SCHOOL OF MEDICINE'),
    ('ROCHESTER', 'UNIVERSITY OF ROCHESTER SCHOOL OF MEDICINE'),
    ('RENO', 'UNIVERSITY OF NEVADA-RENO'),
    ('SAINT LOUIS', 'SAINT LOUIS UNIVERSITY SCHOOL OF MEDICINE'),
    ('ST LOUIS', 'SAINT LOUIS UNIVERSITY SCHOOL OF MEDICINE'),
    ('STANFORD', 'STANFORD UNIVERSITY'),
    # all SUNY
    ('BUFFALO', 'SUNY BUFFALO SCHOOL OF MEDICINE & BIOMEDICAL SCIENCES'),
    ('JACOBS SCHOOL', 'SUNY DOWNSTATE MEDICAL CENTER COLLEGE OF MEDICINE'),
    ('DOWNSTATE', 'SUNY DOWNSTATE MEDICAL CENTER COLLEGE OF MEDICINE'),
    ('UPSTATE', 'SUNY UPSTATE MEDICAL UNIVERSITY AT SYRACUSE'),
    ('SYRACUSE', 'SUNY UPSTATE MEDICAL UNIVERSITY AT SYRACUSE'),
    ('STONY ', 'SUNY HEALTH SCIENCES CENTER AT STONY BROOK SCHOOL OF MEDICINE'),
    ('SUNY HEALTH SCIENCES', 'SUNY HEALTH SCIENCES CENTER AT STONY BROOK SCHOOL OF MEDICINE'),
    ('DOWNSTATE MEDICAL CENTER', 'SUNY DOWNSTATE MEDICAL CENTER COLLEGE OF MEDICINE'),
    ('DOWNSTATE S U N Y', 'SUNY DOWNSTATE MEDICAL CENTER COLLEGE OF MEDICINE'),
    ('UPSTATE MEDICAL', 'SUNY UPSTATE MEDICAL UNIVERSITY AT SYRACUSE'),
    ('N Y DOWNSTATE', 'SUNY DOWNSTATE MEDICAL CENTER COLLEGE OF MEDICINE'),
    #catchall
    ('SUNY', 'SUNY DOWNSTATE MEDICAL CENTER COLLEGE OF MEDICINE'),
    ('TEMPLE ', 'TEMPLE UNIVERSITY SCHOOL OF MEDICINE'),
    ('TEMPLY', 'TEMPLE UNIVERSITY SCHOOL OF MEDICINE'),
    ('TUFTS', 'TUFTS UNIVERSITY SCHOOL OF MEDICINE'),
    ('TUFFS', 'TUFTS UNIVERSITY SCHOOL OF MEDICINE'),
    ('TULANE', 'TULANE UNIVERSITY SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF TENNESSEE', 'UNIVERSITY OF TENNESSEE HEALTH SCIENCE CENTER COLLEGE OF MEDICINE'),
    ('TENNESSEE', 'UNIVERSITY OF TENNESSEE HEALTH SCIENCE CENTER COLLEGE OF MEDICINE'),
    ('FLORIDA', 'UNIVERSITY OF FLORIDA COLLEGE OF MEDICINE'),
    ('OF FLA', 'UNIVERSITY OF FLORIDA COLLEGE OF MEDICINE'),
    ('CALIFORNIA DAVIS', 'UC DAVIS'),
    ('U C DAVIS', 'UC DAVIS SCHOOL OF MEDICINE'),
    ('UC DAVIS', 'UC DAVIS SCHOOL OF MEDICINE'),
    ('UCD UNIVERSITY OF CALIFORNIA', 'UC DAVIS SCHOOL OF MEDICINE'),
    ('IRVINE', 'UC IRVINE COLLEGE OF MEDICINE'),
    ('IRVINE', 'UC IRVINE COLLEGE OF MEDICINE'),
    ('U C S F MEDICAL', 'UCSF SCHOOL OF MEDICINE'),
    ('UCSF ', 'UCSF SCHOOL OF MEDICINE'),
    (' SF ', 'UCSF SCHOOL OF MEDICINE'),
    ('SAN FRANCISCO', 'UCSF SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF CALIFORNIA SF', 'UCSF SCHOOL OF MEDICINE'),
    #catchall
    ('UNIVERSITY OF CALIFORNIA', 'UC SCHOOL OF MEDICINE'),
    ('LOS ANGELES', 'UCLA SCHOOL OF MEDICINE'),
    ('UCLA', 'UCLA SCHOOL OF MEDICINE'),
    ('UCLA', 'UCLA SCHOOL OF MEDICINE'),
    ('BERKELEY', 'UC BERKELEY'),
    ('BERKLEY', 'UC BERKELEY'),
    # CATCHALL
    ('UNIVERSITY OF CALIFORNIA MEDICAL', 'UCSF SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF CAL', 'UCSF SCHOOL OF MEDICINE'),
    ('CALIFORNIA MEDICAL', 'UCSF SCHOOL OF MEDICINE'),

    ('SAN DIEGO', 'UCSD SCHOOL OF MEDICINE'),
    ('UCSD', 'UCSD SCHOOL OF MEDICINE'),
    ('U C S D', 'UCSD SCHOOL OF MEDICINE'),
    # ARBITRARILY ASSIGN UNASSIGN UCAL
    ('UNIVERSITY CALIFORNIA', 'UC'), ('UNIVERSITY OF CALIFORNIA SCHOOL OF MEDICINE', 'UC'),
    ('UMDNJ', 'UMDNJ-NEW JERSEY MEDICAL SCHOOL'),
    ('N J MEDICAL', 'UMDNJ-NEW JERSEY MEDICAL SCHOOL'),
    ('SETON HALL', 'UMDNJ-NEW JERSEY MEDICAL SCHOOL'),
    ('NEW JERSEY', 'UMDNJ-NEW JERSEY MEDICAL SCHOOL'),
    ('RUTGERS', 'UMDNJ-NEW JERSEY MEDICAL SCHOOL'),
    ('COLLEGE OF MEDICINE AND DENTISTRY OF NEW JERSEY', 'UMDNJ-NEW JERSEY MEDICAL SCHOOL'),
    ('UMDNJ NEW JERSEY', 'UMDNJ-NEW JERSEY MEDICAL SCHOOL'),
    ('OF SOUTH CAROLINA', 'UNIVERSITY OF SOUTH CAROLINA SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF S C', 'UNIVERSITY OF SOUTH CAROLINA SCHOOL OF MEDICINE'),
    ('MEDICAL UNVIVERSITY OF SOUTH CAROLINA', 'MEDICAL UNIVERSITY OF SOUTH CAROLINA COLLEGE OF MEDICINE'),
    ('MEDICAL COLLEGE OF SOUTH CAROLINA', 'MEDICAL UNIVERSITY OF SOUTH CAROLINA COLLEGE OF MEDICINE'),

    ('KECK', 'USC KECK SCHOOL OF MEDICINE'), ('SOUTHERN CALIFORNIA', 'USC KECK SCHOOL OF MEDICINE'),
    ('RUSH ', 'RUSH MEDICAL COLLEGE OF RUSH UNIVERSITY'),

    ('UTAH', 'UNIVERSITY OF UTAH SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF WASHINGTON', 'UNIVERSITY OF WASHINGTON SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF WASH', 'UNIVERSITY OF WASHINGTON SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF W MED', 'UNIVERSITY OF WASHINGTON SCHOOL OF MEDICINE'),
    ('WASHINGTON UNIVERSITY', 'WASHINGTON UNIVERSITY SCHOOL OF MEDICINE'),
    ('WASHINGTON MED', 'WASHINGTON UNIVERSITY SCHOOL OF MEDICINE'),
    ('WASHINGTON SCHOOL', 'WASHINGTON UNIVERSITY SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF WASHINGTON', 'UNIVERSITY OF WASHINGTON SCHOOL OF MEDICINE'),
    ('U W SCHOOL OF MEDICINE', 'UNIVERSITY OF WASHINGTON SCHOOL OF MEDICINE'),
    ('HAWAII', 'UNIVERSITY OF HAWAII JOHN A. BURNS SCHOOL OF MEDICINE'),
    ('BURNS SCHOOL', 'UNIVERSITY OF HAWAII JOHN A. BURNS SCHOOL OF MEDICINE'),
    ('SEATTLE', 'UNIVERSITY OF WASHINGTON SCHOOL OF MEDICINE'),
    ('MARQUETTE', 'UNIVERSITY OF WISCONSIN MEDICAL SCHOOL'),
    ('WISCONSIN', 'UNIVERSITY OF WISCONSIN MEDICAL SCHOOL'),
    ('WAKE FOREST', 'WAKE FOREST UNIVERSITY SCHOOL OF MEDICINE'),
    ('BOWMAN GRAY', 'WAKE FOREST UNIVERSITY SCHOOL OF MEDICINE'),
    (' DALLAS', 'UNIVERSITY OF TEXAS SOUTHWESTERN MEDICAL CENTER AT DALLAS'),
    ('TEXAS SOUTHWESTERN', 'UNIVERSITY OF TEXAS SOUTHWESTERN MEDICAL CENTER AT DALLAS'),
    ('TEXAS SOUTH', 'UNIVERSITY OF TEXAS SOUTHWESTERN MEDICAL CENTER AT DALLAS'),
    (' GALVESTON', 'UNIVERSITY OF TEXAS SOUTHWESTERN MEDICAL CENTER AT GALVESTON'),
    ('TEXAS SOUTHWESTERN', 'UNIVERSITY OF TEXAS SOUTHWESTERN MEDICAL CENTER'),
    ('WEST VIRGINIA', 'WEST VIRGINIA UNIVERSITY SCHOOL OF MEDICINE'),
    ('W VA UNIVERSITY', 'WEST VIRGINIA UNIVERSITY SCHOOL OF MEDICINE'),
    ('WAYNE STATE', 'WAYNE STATE UNIVERSITY SCHOOL OF MEDICINE'),
    ('TENNESSEE HEALTH', 'UNIVERSITY OF TENNESSEE HEALTH SCIENCE CENTER COLLEGE OF MEDICINE'),
    ('VERMONT', 'UNIVERSITY OF VERMONT COLLEGE OF MEDICINE'),
    ('ARIZONA', 'UNIVERSITY OF ARIZONA COLLEGE OF MEDICINE'),
    ('COLLEGE OF VIRGINIA', 'MEDICAL COLLEGE OF VIRGINIA'),
    ('COLLEGE OF VA', 'MEDICAL COLLEGE OF VIRGINIA'),
    ('UNIVERSITY OF VIRGINIA', 'UNIVERSITY OF VIRGINIA SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF VA', 'UNIVERSITY OF VIRGINIA SCHOOL OF MEDICINE'),
    ('UNIVERSITY OF CONNECTICUT', 'UNIVERSITY OF CONNECTICUT SCHOOL OF MEDICINE'),
    ('YALE', 'YALE UNIVERSITY SCHOOL OF MEDICINE'),
    ('VANDERBILT', 'VANDERBILT UNIVERSITY SCHOOL OF MEDICINE'),
    ('VANDERVILT', 'VANDERBILT UNIVERSITY SCHOOL OF MEDICINE'),
    ('UNKNOWN', np.nan)]
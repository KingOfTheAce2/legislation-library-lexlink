#!/usr/bin/env python3
"""Validate extracted legal translation terms."""

import csv
from collections import defaultdict
from io import StringIO

# The extracted data
data = """id	source	lang-source	target	lang-target	author	license	sme-reviewed	premium	lang-target-dict
	Verdrag	nl-nl	Abkommen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	Koninkrijk der Nederlanden	nl-nl	Königreich der Niederlande	de-de	van Gassen	All rights reserved	TRUE	FALSE
	Bondsrepubliek Duitsland	nl-nl	Bundesrepublik Deutschland	de-de	van Gassen	All rights reserved	TRUE	FALSE
	dubbele belasting	nl-nl	Doppelbesteuerung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	ontgaan van belasting	nl-nl	Steuerverkürzung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	belastingen naar het inkomen	nl-nl	Steuern vom Einkommen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	rechtspersoon	nl-nl	juristische Person	de-de	van Gassen	All rights reserved	TRUE	FALSE
	plaats van de werkelijke leiding	nl-nl	Ort der tatsächlichen Geschäftsleitung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	grensoverschrijdend bedrijventerrein	nl-nl	grenzüberschreitendes Gewerbegebiet	de-de	van Gassen	All rights reserved	TRUE	FALSE
	gemeenschappelijke grens	nl-nl	gemeinsame Grenze	de-de	van Gassen	All rights reserved	TRUE	FALSE
	vaste bedrijfsinrichting	nl-nl	feste Geschäftseinrichtung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	verdragsluitende staten	nl-nl	Vertragsstaaten	de-de	van Gassen	All rights reserved	TRUE	FALSE
	inwoner	nl-nl	ansässig	de-de	van Gassen	All rights reserved	TRUE	FALSE
	eenduidig vastgesteld	nl-nl	eindeutig bestimmt	de-de	van Gassen	All rights reserved	TRUE	FALSE
	het grootste deel van de gebruikte oppervlakte	nl-nl	größerer Teil der genutzten Fläche	de-de	van Gassen	All rights reserved	TRUE	FALSE
	gebouw	nl-nl	Gebäude	de-de	van Gassen	All rights reserved	TRUE	FALSE
	werkelijke leiding van de onderneming	nl-nl	tatsächliche Geschäftsleitung des Unternehmens	de-de	van Gassen	All rights reserved	TRUE	FALSE
	vloeroppervlak gebruikt door de onderneming	nl-nl	vom Unternehmen genutzte Fläche	de-de	van Gassen	All rights reserved	TRUE	FALSE
	recht tot belastingheffing	nl-nl	Besteuerungsrecht	de-de	van Gassen	All rights reserved	TRUE	FALSE
	voorbeelden	nl-nl	Beispielsfälle	de-de	van Gassen	All rights reserved	TRUE	FALSE
	voorbeeld	nl-nl	Beispielsfall	de-de	van Gassen	All rights reserved	TRUE	FALSE
	onderneming	nl-nl	Unternehmen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	inkomsten van de onderneming	nl-nl	Gewinne des Unternehmens	de-de	van Gassen	All rights reserved	TRUE	FALSE
	economische betrekkingen	nl-nl	wirtschaftlichen Beziehungen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	samenwerking op het gebied van belastingzaken	nl-nl	Zusammenarbeit in Steuersachen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	doeltreffende en juiste belastingheffing	nl-nl	wirksame und zutreffende Steuererhebung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	heffingsbevoegdheden	nl-nl	Besteuerungsrechte	de-de	van Gassen	All rights reserved	TRUE	FALSE
	vermijden van dubbele heffing	nl-nl	Vermeidung der Doppelbesteuerung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	personen die inwoner zijn van een verdragsluitende staat	nl-nl	Personen, die in einem Vertragsstaat ansässig sind	de-de	van Gassen	All rights reserved	TRUE	FALSE
	belastingen naar het gehele inkomen	nl-nl	Steuern, die vom Gesamteinkommen erhoben werden	de-de	van Gassen	All rights reserved	TRUE	FALSE
	roerende of onroerende zaken	nl-nl	beweglichen oder unbeweglichen Vermögens	de-de	van Gassen	All rights reserved	TRUE	FALSE
	loonbelasting	nl-nl	Lohnsummensteuern	de-de	van Gassen	All rights reserved	TRUE	FALSE
	ondernemingsbelasting	nl-nl	Gewerbesteuer	de-de	van Gassen	All rights reserved	TRUE	FALSE
	mijnbouwwet	nl-nl	Bergbaugesetz	de-de	van Gassen	All rights reserved	TRUE	FALSE
	bevoegde autoriteiten	nl-nl	zuständigen Behörden	de-de	van Gassen	All rights reserved	TRUE	FALSE
	wezenlijke wijzigingen	nl-nl	wesentlichen Änderungen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	algemene begripsomschrijvingen	nl-nl	Allgemeine Begriffsbestimmungen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	verdragsluitende staat	nl-nl	Vertragsstaat	de-de	van Gassen	All rights reserved	TRUE	FALSE
	Duitsland	nl-nl	Deutschland	de-de	van Gassen	All rights reserved	TRUE	FALSE
	Nederland	nl-nl	Niederlande	de-de	van Gassen	All rights reserved	TRUE	FALSE
	persoon	nl-nl	Person	de-de	van Gassen	All rights reserved	TRUE	FALSE
	lichaam	nl-nl	Gesellschaft	de-de	van Gassen	All rights reserved	TRUE	FALSE
	bedrijfsuitoefening	nl-nl	Geschäftstätigkeit	de-de	van Gassen	All rights reserved	TRUE	FALSE
	internationaal verkeer	nl-nl	internationaler Verkehr	de-de	van Gassen	All rights reserved	TRUE	FALSE
	onderdaan	nl-nl	Staatsangehöriger	de-de	van Gassen	All rights reserved	TRUE	FALSE
	bevoegde autoriteit	nl-nl	zuständige Behörde	de-de	van Gassen	All rights reserved	TRUE	FALSE
	inwoner	nl-nl	ansässige Person	de-de	van Gassen	All rights reserved	TRUE	FALSE
	duurzaam tehuis	nl-nl	ständige Wohnstätte	de-de	van Gassen	All rights reserved	TRUE	FALSE
	middelpunt van de levensbelangen	nl-nl	Mittelpunkt der Lebensinteressen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	gewoonlijk verblijft	nl-nl	gewöhnlichen Aufenthalt	de-de	van Gassen	All rights reserved	TRUE	FALSE
	plaats van de werkelijke leiding	nl-nl	Ort der tatsächlichen Geschäftsleitung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	vaste inrichting	nl-nl	Betriebsstätte	de-de	van Gassen	All rights reserved	TRUE	FALSE
	werkzaamheden buitengaats	nl-nl	Tätigkeiten vor der Küste	de-de	van Gassen	All rights reserved	TRUE	FALSE
	bouwwerk of constructiewerkzaamheden	nl-nl	Bauausführung oder Montage	de-de	van Gassen	All rights reserved	TRUE	FALSE
	makelaar of commissionair	nl-nl	Makler oder Kommissionär	de-de	van Gassen	All rights reserved	TRUE	FALSE
	onafhankelijke vertegenwoordiger	nl-nl	unabhängiger Vertreter	de-de	van Gassen	All rights reserved	TRUE	FALSE
	filiaal	nl-nl	Zweigniederlassung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	fabriek	nl-nl	Fabrikationsstätte	de-de	van Gassen	All rights reserved	TRUE	FALSE
	werkplaats	nl-nl	Werkstätte	de-de	van Gassen	All rights reserved	TRUE	FALSE
	mijn	nl-nl	Bergwerk	de-de	van Gassen	All rights reserved	TRUE	FALSE
	olie- of gasbron	nl-nl	Öl- oder Gasvorkommen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	(steen)groeve	nl-nl	Steinbruch	de-de	van Gassen	All rights reserved	TRUE	FALSE
	natuurlijke rijkdommen	nl-nl	natürliche Ressourcen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	inkomsten uit onroerende zaken	nl-nl	Einkünfte aus unbeweglichem Vermögen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	onroerende zaken	nl-nl	unbewegliches Vermögen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	landbouw- of bosbedrijven	nl-nl	land- und forstwirtschaftliche Betriebe	de-de	van Gassen	All rights reserved	TRUE	FALSE
	vruchtgebruik	nl-nl	Nutzungsrechte	de-de	van Gassen	All rights reserved	TRUE	FALSE
	minerale aardlagen	nl-nl	Mineralvorkommen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	bronnen en andere natuurlijke rijkdommen	nl-nl	Quellen und andere natürliche Ressourcen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	winst uit onderneming	nl-nl	Unternehmensgewinne	de-de	van Gassen	All rights reserved	TRUE	FALSE
	vaste inrichting	nl-nl	Betriebsstätte	de-de	van Gassen	All rights reserved	TRUE	FALSE
	zeevaart, binnenvaart en luchtvervoer	nl-nl	Seeschifffahrt, Binnenschifffahrt und Luftfahrt	de-de	van Gassen	All rights reserved	TRUE	FALSE
	schepen of luchtvaartuigen in internationaal verkeer	nl-nl	Seeschiffe oder Luftfahrzeuge im internationalen Verkehr	de-de	van Gassen	All rights reserved	TRUE	FALSE
	binnenschepen	nl-nl	Binnenschiffe	de-de	van Gassen	All rights reserved	TRUE	FALSE
	containers	nl-nl	Container	de-de	van Gassen	All rights reserved	TRUE	FALSE
	pool	nl-nl	Pool	de-de	van Gassen	All rights reserved	TRUE	FALSE
	gemeenschappelijke onderneming	nl-nl	Betriebsgemeinschaft	de-de	van Gassen	All rights reserved	TRUE	FALSE
	gelieerde ondernemingen	nl-nl	verbundene Unternehmen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	handelsbetrekkingen of financiële betrekkingen	nl-nl	kaufmännischen oder finanziellen Beziehungen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	dividenden	nl-nl	Dividenden	de-de	van Gassen	All rights reserved	TRUE	FALSE
	pensioenfonds	nl-nl	Pensionsfonds	de-de	van Gassen	All rights reserved	TRUE	FALSE
	winstaandelen of winstbewijzen	nl-nl	Genussrechte oder Genussscheine	de-de	van Gassen	All rights reserved	TRUE	FALSE
	mijnaandelen	nl-nl	Kuxen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	oprichtersaandelen	nl-nl	Gründeranteile	de-de	van Gassen	All rights reserved	TRUE	FALSE
	interest	nl-nl	Zinsen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	schuldvorderingen	nl-nl	Forderungen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	obligaties	nl-nl	Obligationen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	schuldbewijzen	nl-nl	Losanleihen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	boetes voor te late betaling	nl-nl	Zuschläge für verspätete Zahlung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	royalty's	nl-nl	Lizenzgebühren	de-de	van Gassen	All rights reserved	TRUE	FALSE
	auteursrecht	nl-nl	Urheberrechten	de-de	van Gassen	All rights reserved	TRUE	FALSE
	octrooi	nl-nl	Patenten	de-de	van Gassen	All rights reserved	TRUE	FALSE
	fabrieks- of handelsmerk	nl-nl	Warenzeichen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	tekening of model	nl-nl	Muster oder Modellen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	geheim recept of geheime werkwijze	nl-nl	geheime Formeln oder Verfahren	de-de	van Gassen	All rights reserved	TRUE	FALSE
	ervaringen op het gebied van nijverheid, handel of wetenschap	nl-nl	gewerblicher, kaufmännischer oder wissenschaftlicher Erfahrungen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	vermogenswinsten	nl-nl	Gewinne aus der Veräußerung von Vermögen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	vervreemding van onroerende zaken	nl-nl	Veräußerung unbeweglichen Vermögens	de-de	van Gassen	All rights reserved	TRUE	FALSE
	aandelen of vergelijkbare belangen	nl-nl	Aktien oder vergleichbaren Anteilen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	erkende effectenbeurs	nl-nl	anerkannte Börse	de-de	van Gassen	All rights reserved	TRUE	FALSE
	bedrijfsvermogen	nl-nl	Betriebsvermögen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	roerende zaken	nl-nl	beweglichen Vermögens	de-de	van Gassen	All rights reserved	TRUE	FALSE
	vervreemder	nl-nl	Veräußerer	de-de	van Gassen	All rights reserved	TRUE	FALSE
	waardevermeerdering van vermogen	nl-nl	Vermögenszuwachs	de-de	van Gassen	All rights reserved	TRUE	FALSE
	inkomsten uit dienstbetrekking	nl-nl	Einkünfte aus unselbständiger Arbeit	de-de	van Gassen	All rights reserved	TRUE	FALSE
	dienstbetrekking	nl-nl	unselbständige Arbeit	de-de	van Gassen	All rights reserved	TRUE	FALSE
	salarissen, lonen en andere soortgelijke beloningen	nl-nl	Gehälter, Löhne und ähnliche Vergütungen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	verordening (EEG) 1408/71	nl-nl	Verordnung (EWG) Nr. 1408/71	de-de	van Gassen	All rights reserved	TRUE	FALSE
	verordening (EG) 883/2004	nl-nl	Verordnung (EG) Nr. 883/2004	de-de	van Gassen	All rights reserved	TRUE	FALSE
	directeursbeloningen	nl-nl	Aufsichtsrats- oder Verwaltungsratsvergütungen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	lid van de raad van beheer	nl-nl	Mitglied des Aufsichts- oder Verwaltungsrats	de-de	van Gassen	All rights reserved	TRUE	FALSE
	artiesten en sportbeoefenaars	nl-nl	Künstler und Sportler	de-de	van Gassen	All rights reserved	TRUE	FALSE
	toneelspeler, film-, radio- of televisie-artiest of musicus	nl-nl	Bühnen-, Film-, Rundfunk- und Fernsehkünstler sowie Musiker	de-de	van Gassen	All rights reserved	TRUE	FALSE
	persoonlijke werkzaamheden	nl-nl	persönlich ausgeübte Tätigkeit	de-de	van Gassen	All rights reserved	TRUE	FALSE
	socialezekerheidsuitkeringen	nl-nl	Sozialversicherungsleistungen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	pensioenen en lijfrenten	nl-nl	Ruhegehälter und Renten	de-de	van Gassen	All rights reserved	TRUE	FALSE
	socialezekerheidspensioenen	nl-nl	Sozialversicherungsrenten	de-de	van Gassen	All rights reserved	TRUE	FALSE
	periodieke betalingen	nl-nl	regelmäßig wiederkehrender Art	de-de	van Gassen	All rights reserved	TRUE	FALSE
	schadevergoeding wegens politieke vervolging	nl-nl	Entschädigung für politische Verfolgung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	algemene belang	nl-nl	öffentlichen Interesse	de-de	van Gassen	All rights reserved	TRUE	FALSE
	overheidsfuncties	nl-nl	öffentlicher Dienst	de-de	van Gassen	All rights reserved	TRUE	FALSE
	bezoekende hoogleraren en docenten	nl-nl	Gastprofessoren und Lehrer	de-de	van Gassen	All rights reserved	TRUE	FALSE
	studenten	nl-nl	Studenten	de-de	van Gassen	All rights reserved	TRUE	FALSE
	overige inkomsten	nl-nl	Andere Einkünfte	de-de	van Gassen	All rights reserved	TRUE	FALSE
	vermijden van dubbele belasting	nl-nl	vermeidung der Doppelbesteuerung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	belastinggrondslag	nl-nl	Bemessungsgrundlage	de-de	van Gassen	All rights reserved	TRUE	FALSE
	bestanddeel van het inkomen	nl-nl	Einkünfte	de-de	van Gassen	All rights reserved	TRUE	FALSE
	werkelijk wordt belast	nl-nl	tatsächlich besteuert werden	de-de	van Gassen	All rights reserved	TRUE	FALSE
	samenwerkingsverband	nl-nl	Personengesellschaft	de-de	van Gassen	All rights reserved	TRUE	FALSE
	kapitaal	nl-nl	Kapital	de-de	van Gassen	All rights reserved	TRUE	FALSE
	winst van het lichaam	nl-nl	Gewinne der ausschüttenden Gesellschaft	de-de	van Gassen	All rights reserved	TRUE	FALSE
	verrekening van buitenlandse belasting	nl-nl	Anrechnung ausländischer Steuern	de-de	van Gassen	All rights reserved	TRUE	FALSE
	ingevolge het Nederlandse belastingrecht	nl-nl	nach niederländischem Recht	de-de	van Gassen	All rights reserved	TRUE	FALSE
	directeursbeloningen	nl-nl	Aufsichtsrats- und Verwaltungsratsvergütungen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	pensioenen, lijfrenten en socialezekerheidsuitkeringen	nl-nl	Ruhegehälter, Renten und Sozialversicherungsleistungen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	belastingtarief	nl-nl	Steuersatz	de-de	van Gassen	All rights reserved	TRUE	FALSE
	diplomatieke weg	nl-nl	diplomatischem Weg	de-de	van Gassen	All rights reserved	TRUE	FALSE
	belastingverrekening	nl-nl	Steueranrechnung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	Tweede Wereldoorlog	nl-nl	Zweiten Weltkrieg	de-de	van Gassen	All rights reserved	TRUE	FALSE
	dwangarbeider	nl-nl	Zwangsarbeiter	de-de	van Gassen	All rights reserved	TRUE	FALSE
	invaliditeitspensioenen	nl-nl	Verletztenrenten	de-de	van Gassen	All rights reserved	TRUE	FALSE
	socialezekerheidswetgeving	nl-nl	Sozialversicherungsgesetze	de-de	van Gassen	All rights reserved	TRUE	FALSE
	belastingvermindering	nl-nl	Steuerermäßigung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	fiscale faciliëring	nl-nl	Steuervergünstigung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	belasting over deze bestanddelen van het inkomen	nl-nl	Steuer auf diese Einkünfte	de-de	van Gassen	All rights reserved	TRUE	FALSE
	wettelijke vereisten	nl-nl	rechtlichen Voraussetzungen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	Toepassing van het Verdrag in bijzondere gevallen	nl-nl	Anwendung des Abkommens in bestimmten Fällen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	non-discriminatie	nl-nl	Gleichbehandlung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	onderdanen	nl-nl	Staatsangehörige	de-de	van Gassen	All rights reserved	TRUE	FALSE
	staatlozen	nl-nl	Staatenlose	de-de	van Gassen	All rights reserved	TRUE	FALSE
	vaste inrichting	nl-nl	Betriebsstätte	de-de	van Gassen	All rights reserved	TRUE	FALSE
	persoonlijke aftrekken, tegemoetkomingen en verminderingen	nl-nl	Steuerfreibeträge, -vergünstigungen und -ermäßigungen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	interest, royalty's en andere uitgaven	nl-nl	Zinsen, Lizenzgebühren und andere Entgelte	de-de	van Gassen	All rights reserved	TRUE	FALSE
	pensioenregeling	nl-nl	Altersversorgungssystem	de-de	van Gassen	All rights reserved	TRUE	FALSE
	publiekrechtelijk socialezekerheidsstelsel	nl-nl	staatlichen Sozialversicherungssystems	de-de	van Gassen	All rights reserved	TRUE	FALSE
	procedure voor onderling overleg	nl-nl	Verständigungsverfahren	de-de	van Gassen	All rights reserved	TRUE	FALSE
	boekenonderzoeken op grensoverschrijdende bedrijventerreinen	nl-nl	Außenprüfungen in grenzüberschreitenden Gewerbegebieten	de-de	van Gassen	All rights reserved	TRUE	FALSE
	uitwisseling van informatie	nl-nl	Informationsaustausch	de-de	van Gassen	All rights reserved	TRUE	FALSE
	bijstand bij de invordering van belastingen	nl-nl	Amtshilfe bei der Erhebung von Steuern	de-de	van Gassen	All rights reserved	TRUE	FALSE
	procedures voor belastingheffing aan de bron	nl-nl	Verfahrensregeln für die Quellenbesteuerung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	leden van diplomatieke vertegenwoordigingen en consulaire posten	nl-nl	Mitglieder diplomatischer Missionen und konsularischer Vertretungen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	bijlage en Protocol	nl-nl	Anlage und Protokoll	de-de	van Gassen	All rights reserved	TRUE	FALSE
	uitbreiding tot andere gebieden	nl-nl	Ausweitung des räumlichen Geltungsbereichs	de-de	van Gassen	All rights reserved	TRUE	FALSE
	inwerkingtreding	nl-nl	Inkrafttreten	de-de	van Gassen	All rights reserved	TRUE	FALSE
	bekrachtiging	nl-nl	Ratifikation	de-de	van Gassen	All rights reserved	TRUE	FALSE
	akten van bekrachtiging	nl-nl	Ratifikationsurkunden	de-de	van Gassen	All rights reserved	TRUE	FALSE
	in werking treden	nl-nl	in Kraft treten	de-de	van Gassen	All rights reserved	TRUE	FALSE
	belastingen geheven aan de bron	nl-nl	im Abzugsweg erhobenen Steuern	de-de	van Gassen	All rights reserved	TRUE	FALSE
	overige belastingen	nl-nl	übrigen Steuern	de-de	van Gassen	All rights reserved	TRUE	FALSE
	kalenderjaar	nl-nl	Kalenderjahr	de-de	van Gassen	All rights reserved	TRUE	FALSE
	Overeenkomst van 1959	nl-nl	Abkommen von 1959	de-de	van Gassen	All rights reserved	TRUE	FALSE
	Aanvullend Protocol	nl-nl	Zusatzprotokoll	de-de	van Gassen	All rights reserved	TRUE	FALSE
	Tweede Aanvullend Protocol	nl-nl	Zweite Zusatzprotokoll	de-de	van Gassen	All rights reserved	TRUE	FALSE
	Derde Aanvullend Protocol	nl-nl	Dritte Zusatzprotokoll	de-de	van Gassen	All rights reserved	TRUE	FALSE
	openstaande gevallen	nl-nl	offenen Fällen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	belastingen, belastingjaren en -tijdvakken	nl-nl	Steuern, Veranlagungsjahre und -zeiträume	de-de	van Gassen	All rights reserved	TRUE	FALSE
	voordelen	nl-nl	Vergünstigungen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	beëindiging	nl-nl	Kündigung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	beëindigen	nl-nl	kündigen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	kennisgeving van beëindiging	nl-nl	Kündigung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	langs diplomatieke weg	nl-nl	auf diplomatischem Weg	de-de	van Gassen	All rights reserved	TRUE	FALSE
	verstrijken van een tijdvak van vijf jaar	nl-nl	Ablauf von fünf Jahren	de-de	van Gassen	All rights reserved	TRUE	FALSE
	GEDAAN te Berlijn	nl-nl	GESCHEHEN zu Berlin	de-de	van Gassen	All rights reserved	TRUE	FALSE
	Onderlinge overeenkomst tussen het Koninkrijk der Nederlanden en de Bondsrepubliek Duitsland	nl-nl	Verständigungsvereinbarung zwischen dem Königreich der Niederlande und der Bundesrepublik Deutschland	de-de	van Gassen	All rights reserved	TRUE	FALSE
	arbitrageprocedure	nl-nl	Schiedsverfahren	de-de	van Gassen	All rights reserved	TRUE	FALSE
	verzoek om arbitrage	nl-nl	Schiedsantrag	de-de	van Gassen	All rights reserved	TRUE	FALSE
	arbiters	nl-nl	Schiedsrichter	de-de	van Gassen	All rights reserved	TRUE	FALSE
	voorzitter	nl-nl	Vorsitzender	de-de	van Gassen	All rights reserved	TRUE	FALSE
	hoogstgeplaatste functionaris van het Secretariaat van het Centre for Tax Policy and Administration van de OESO	nl-nl	hochrangigste Mitglied des Sekretariats des Zentrums für Steuerpolitik und Steuerverwaltung der OECD	de-de	van Gassen	All rights reserved	TRUE	FALSE
	gestroomlijnde arbitrageprocedure	nl-nl	vereinfachtes Schiedsverfahren	de-de	van Gassen	All rights reserved	TRUE	FALSE
	vertrouwelijkheid	nl-nl	Vertraulichkeit	de-de	van Gassen	All rights reserved	TRUE	FALSE
	procedure en bewijsvoering	nl-nl	Verfahrens- und Beweisregeln	de-de	van Gassen	All rights reserved	TRUE	FALSE
	deelname door de persoon die om de arbitrage heeft verzocht	nl-nl	Beteiligung des Antragstellers	de-de	van Gassen	All rights reserved	TRUE	FALSE
	logistieke maatregelen	nl-nl	Organisatorisches	de-de	van Gassen	All rights reserved	TRUE	FALSE
	kosten	nl-nl	Kosten	de-de	van Gassen	All rights reserved	TRUE	FALSE
	toepasselijke rechtsbeginselen	nl-nl	anzuwendende Rechtsgrundsätze	de-de	van Gassen	All rights reserved	TRUE	FALSE
	arbitrale uitspraak	nl-nl	Schiedsspruch	de-de	van Gassen	All rights reserved	TRUE	FALSE
	definitieve uitspraak	nl-nl	Endgültige Entscheidung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	tenuitvoerlegging van de arbitrale uitspraak	nl-nl	Umsetzung des Schiedsspruchs	de-de	van Gassen	All rights reserved	TRUE	FALSE
	Europees Parlement	nl-nl	Europäisches Parlament	de-de	van Gassen	All rights reserved	TRUE	FALSE
	stille vennoot	nl-nl	stiller Gesellschafter	de-de	van Gassen	All rights reserved	TRUE	FALSE
	lening met een rentepercentage gekoppeld aan de winst van de schuldenaar	nl-nl	partiarisches Darlehen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	obligaties met winstdeling	nl-nl	Gewinnobligationen	de-de	van Gassen	All rights reserved	TRUE	FALSE
	besloten fondsen voor gemene rekening	nl-nl	geschlossene Fonds für gemeinsame Rechnung	de-de	van Gassen	All rights reserved	TRUE	FALSE
	investeringsregelingen of samenwerkingsverbanden	nl-nl	Investmentvermögen oder Personengesellschaften	de-de	van Gassen	All rights reserved	TRUE	FALSE"""

def main():
    """Main validation function."""
    reader = csv.DictReader(StringIO(data), delimiter='\t')
    rows = list(reader)

    print(f"Total terms extracted: {len(rows)}\n")

    # Track duplicates
    source_terms = defaultdict(list)
    target_terms = defaultdict(list)
    source_target_pairs = defaultdict(int)

    # Track empty fields
    empty_ids = 0
    empty_lang_target_dict = 0

    for idx, row in enumerate(rows, 1):
        source = row.get('source', '').strip() if row.get('source') else ''
        target = row.get('target', '').strip() if row.get('target') else ''

        # Check for empty fields
        row_id = row.get('id', '') or ''
        if not row_id.strip():
            empty_ids += 1
        lang_target_dict = row.get('lang-target-dict', '') or ''
        if not lang_target_dict.strip():
            empty_lang_target_dict += 1

        # Track duplicates
        source_terms[source].append(idx)
        target_terms[target].append(idx)
        source_target_pairs[(source, target)] += 1

    # Report findings
    print("=" * 80)
    print("VALIDATION REPORT")
    print("=" * 80)

    print("\n1. MISSING DATA:")
    print(f"   - Empty 'id' fields: {empty_ids}/{len(rows)}")
    print(f"   - Empty 'lang-target-dict' fields: {empty_lang_target_dict}/{len(rows)}")

    print("\n2. DUPLICATE SOURCE TERMS (Dutch):")
    duplicates_found = False
    for term, occurrences in sorted(source_terms.items()):
        if len(occurrences) > 1:
            duplicates_found = True
            print(f"   - '{term}' appears {len(occurrences)} times (rows: {', '.join(map(str, occurrences))})")
            for occ in occurrences:
                src = rows[occ-1].get('source', '') or ''
                tgt = rows[occ-1].get('target', '') or ''
                print(f"     -> Row {occ}: {src} -> {tgt}")
    if not duplicates_found:
        print("   [OK] No duplicate source terms")

    print("\n3. DUPLICATE TARGET TERMS (German):")
    duplicates_found = False
    for term, occurrences in sorted(target_terms.items()):
        if len(occurrences) > 1:
            duplicates_found = True
            print(f"   - '{term}' appears {len(occurrences)} times (rows: {', '.join(map(str, occurrences))})")
    if not duplicates_found:
        print("   [OK] No duplicate target terms")

    print("\n4. EXACT DUPLICATE PAIRS:")
    exact_duplicates = [(pair, count) for pair, count in source_target_pairs.items() if count > 1]
    if exact_duplicates:
        for (source, target), count in exact_duplicates:
            print(f"   - '{source}' -> '{target}' appears {count} times")
    else:
        print("   [OK] No exact duplicate translation pairs")

    print("\n5. DATA CONSISTENCY:")
    all_consistent = True
    for row in rows:
        if row.get('lang-source') != 'nl-nl':
            print(f"   [X] Inconsistent source language: {row.get('lang-source')}")
            all_consistent = False
        if row.get('lang-target') != 'de-de':
            print(f"   [X] Inconsistent target language: {row.get('lang-target')}")
            all_consistent = False
        if row.get('author') != 'van Gassen':
            print(f"   [X] Inconsistent author: {row.get('author')}")
            all_consistent = False
        if row.get('sme-reviewed') != 'TRUE':
            print(f"   [X] Not SME reviewed: {row.get('source')}")
            all_consistent = False
    if all_consistent:
        print("   [OK] All metadata fields are consistent")

    print("\n6. TRANSLATION QUALITY SPOT CHECK:")
    spot_check = [
        ("Verdrag", "Abkommen", "Treaty/Agreement"),
        ("dubbele belasting", "Doppelbesteuerung", "Double taxation"),
        ("vaste inrichting", "Betriebsstätte", "Permanent establishment"),
        ("belastingverdrag", "Steuerabkommen", "Tax treaty"),
    ]

    for nl_term, expected_de, meaning in spot_check:
        matches = [row for row in rows if row.get('source') == nl_term]
        if matches:
            actual_de = matches[0].get('target', '')
            status = "[OK]" if actual_de == expected_de else "[?]"
            print(f"   {status} '{nl_term}' -> '{actual_de}' ({meaning})")
        else:
            print(f"   - '{nl_term}' not found in extraction")

    print("\n" + "=" * 80)
    print("RECOMMENDATIONS:")
    print("=" * 80)
    print("\n1. Generate UUIDs for the 'id' field")
    print("2. Decide on strategy for duplicate source terms:")
    print("   - Keep context-dependent variations")
    print("   - OR merge with usage notes")
    print("3. Populate 'lang-target-dict' if needed for dictionary references")
    print("4. Consider adding:")
    print("   - Definition/context field")
    print("   - Example sentences")
    print("   - Term frequency/importance score")
    print("   - Article/section reference from source XML")
    print("\n")

if __name__ == "__main__":
    main()

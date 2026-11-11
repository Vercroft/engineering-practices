# FSL-1.1-MIT for public products sold as a hosted service

Date: 2026-11-11
Status: accepted

## Context

A product sold as a hosted service asks its users to trust it with their data. Users can only check what it does with
that data if they can read its code, server included, so the code has to be public. The paid features stay in a separate
private repository, as standard §7F.1 says.

None of the three code licences in standard §7F.2 fits. MIT lets anyone, a competitor included, take the code and sell
the same service. PolyForm Strict allows noncommercial use only and forbids changes, so it rules out the use our users
need, such as running the code for their own work. All rights reserved is not inspectable at all.

The Functional Source License was written for this case. Its authors describe it as "tuned for SaaS companies" and
"less restrictive than copyleft, and more open than open core"
([announcement](https://blog.sentry.io/introducing-the-functional-source-license-freedom-without-free-riding)).

## Decision

We will license a public product that is sold as a hosted service under FSL-1.1-MIT, and add it to standard §7F.2 as a
fourth code licence. It permits every purpose except a Competing Use, meaning making the Software available to others in
a commercial product or service that substitutes for the Software, substitutes for any other product or service we offer
using the Software that exists as of the date we make the Software available, or offers the same or substantially
similar functionality as the Software. Its permitted purposes specifically include internal use and access,
non-commercial education, non-commercial research, and professional services provided to a licensee using the Software.
Each version becomes available under MIT on the second anniversary of the date it was made available
([template](https://fsl.software/FSL-1.1-MIT.template.md)). Its SPDX identifier is `FSL-1.1-MIT`
([SPDX](https://spdx.org/licenses/FSL-1.1-MIT.html)). The server code of such a product is public on purpose, so §7F.1
now makes that one exception; paid features and secret logic stay private.

## Consequences

Users can read, run and change the code for any purpose that does not compete with the product, and after two years each
version is plain MIT. A competitor cannot sell the same service from our code during that time. The cost is that the
code is source-available for two years and open source only after that, so the product is not described as open source
before then. Adopters who need a different split choose one of the other licences in §7F.2.
